"""塔罗牌业务逻辑服务"""
import os
from data.tarot_deck import get_card_by_id, get_deck_size
from data.spreads import Spread, get_spread_by_id
from data.tarot_skills import apply_skill_to_reading, TAROT_SKILLS
from services.random_service import RandomService
from services.llm_service import LLMService


class TarotService:
    """塔罗牌服务类"""
    
    def __init__(self):
        self.random_service = RandomService()
        self.llm_service = LLMService()
        self.prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'prompts')
    
    def _resolve_spread(self, spread_id, custom_spread=None):
        """获取固定牌阵或根据请求构建自定义牌阵"""
        if custom_spread:
            name_cn = custom_spread.get('name') or custom_spread.get('name_cn') or '自定义牌阵'
            description = custom_spread.get('description') or '根据当前问题定制的位置解读'
            positions = custom_spread.get('positions') or []

            clean_positions = []
            for position in positions[:10]:
                if isinstance(position, dict):
                    position_name = str(position.get('name', '')).strip()
                    position_description = str(position.get('description', '')).strip()
                else:
                    position_name = str(position).strip()
                    position_description = ''

                if position_name:
                    clean_positions.append({
                        'name': position_name[:40],
                        'description': position_description[:120] or position_name[:40]
                    })

            if not 1 <= len(clean_positions) <= 10:
                raise ValueError("自定义牌阵需要 1-10 个有效位置")

            return Spread(
                id='custom',
                name='Custom Spread',
                name_cn=name_cn[:40],
                description=description[:160],
                cards=len(clean_positions),
                positions=clean_positions
            )

        spread = get_spread_by_id(spread_id)
        if not spread:
            raise ValueError(f"无效的牌阵 ID: {spread_id}")
        return spread

    def draw_cards(self, spread_id, custom_spread=None):
        """
        抽牌
        
        Args:
            spread_id: 牌阵 ID
            custom_spread: 可选的自定义牌阵定义
            
        Returns:
            list: 抽取的牌信息列表
        """
        spread = self._resolve_spread(spread_id, custom_spread)
        deck_size = get_deck_size()
        card_count = spread.cards
        
        # 真随机抽牌
        indices, orientations = self.random_service.draw_cards(deck_size, card_count)
        
        # 构建结果
        result = []
        for idx, orientation in zip(indices, orientations):
            card = get_card_by_id(idx)
            if card:
                card_dict = card.to_dict()
                card_dict['orientation'] = orientation
                result.append(card_dict)
        
        return result

    def normalize_drawn_cards(self, spread_id, cards, custom_spread=None):
        """
        只信任客户端传回的牌 ID 和正逆位，其他牌义字段全部由服务端牌库重建。
        这样可以避免用户篡改 cards payload 向 Prompt 注入任意内容。
        """
        spread = self._resolve_spread(spread_id, custom_spread)
        if not isinstance(cards, list) or len(cards) != spread.cards:
            raise ValueError(f"牌面数量必须为 {spread.cards} 张")

        normalized = []
        seen_ids = set()
        for card_data in cards:
            if not isinstance(card_data, dict):
                raise ValueError("卡牌信息格式错误")

            try:
                card_id = int(card_data.get('id'))
            except (TypeError, ValueError):
                raise ValueError("卡牌 ID 无效")

            if card_id in seen_ids:
                raise ValueError("卡牌不能重复")
            seen_ids.add(card_id)

            orientation = card_data.get('orientation')
            if orientation not in ('upright', 'reversed'):
                raise ValueError("卡牌正逆位无效")

            card = get_card_by_id(card_id)
            if not card:
                raise ValueError("卡牌不存在")

            clean_card = card.to_dict()
            clean_card['orientation'] = orientation
            normalized.append(clean_card)

        return normalized
    
    def build_prompt(self, question, spread_id, cards, custom_spread=None, reader_style=None):
        """
        构建 Prompt
        
        Args:
            question: 用户问题
            spread_id: 牌阵 ID
            cards: 抽取的牌列表
            custom_spread: 可选的自定义牌阵定义
            reader_style: 可选的解读风格
            
        Returns:
            str: 完整的 Prompt
        """
        spread = self._resolve_spread(spread_id, custom_spread)

        # 读取基础 Prompt 模板
        base_prompt_path = os.path.join(self.prompts_dir, 'base.txt')
        with open(base_prompt_path, 'r', encoding='utf-8') as f:
            base_template = f.read()
        
        # 读取特定牌阵的 Prompt 模板
        specific_prompt_path = os.path.join(self.prompts_dir, f'{spread_id}.txt')
        if os.path.exists(specific_prompt_path):
            with open(specific_prompt_path, 'r', encoding='utf-8') as f:
                specific_instructions = f.read()
        else:
            specific_instructions = ""

        if reader_style:
            style_instructions = {
                'gentle': '解读风格：温柔支持。请用安定、共情的语气表达，同时保留清晰建议。',
                'direct': '解读风格：直接清醒。请减少委婉铺垫，指出关键问题、风险和行动重点。',
                'psychology': '解读风格：心理洞察。请更多分析动机、投射、关系模式和内在需求。',
                'practical': '解读风格：现实行动。请把重点放在可执行步骤、优先级和短期决策上。'
            }
            specific_instructions = '\n\n'.join([
                specific_instructions,
                style_instructions.get(reader_style, str(reader_style)[:120])
            ]).strip()
        
        # 构建卡牌描述
        cards_description = []
        for i, card_data in enumerate(cards):
            position = spread.positions[i]
            orientation = card_data['orientation']
            meaning_data = card_data[orientation]
            
            card_desc = f"""
位置 {i + 1}: {position['name']} ({position['description']})
牌: {card_data['name_cn']} ({card_data['name']}) - {orientation == 'upright' and '正位' or '逆位'}
关键词: {', '.join(meaning_data['keywords'])}
含义: {meaning_data['meaning']}
元素: {card_data['element'] or '无'}
星象: {card_data['astrology'] or '无'}
"""
            cards_description.append(card_desc.strip())
        
        # 填充模板
        prompt = base_template.format(
            question=question,
            spread_name=spread.name_cn,
            spread_name_en=spread.name,
            spread_description=spread.description,
            cards_description='\n\n'.join(cards_description),
            specific_instructions=specific_instructions
        )

        # 🔮 应用 Tarot Skills（如果抽到大阿尔卡纳）
        # 检查是否有大阿尔卡纳牌，如果有，应用其技能模式
        major_cards = [card for card in cards if card['type'] == 'major' and card['id'] < 22]
        if major_cards:
            # 使用第一张大阿尔卡纳的技能
            primary_major = major_cards[0]
            card_id = primary_major['id']

            if card_id in TAROT_SKILLS:
                skill = TAROT_SKILLS[card_id]
                print(f"🎴 应用 Tarot Skill: {skill['name']} - {skill['skill_name']}")
                prompt = apply_skill_to_reading(card_id, prompt)

        return prompt
    
    def get_reading_stream(self, question, spread_id, cards, custom_spread=None, reader_style=None):
        """
        获取流式解读
        
        Args:
            question: 用户问题
            spread_id: 牌阵 ID
            cards: 抽取的牌列表
            custom_spread: 可选的自定义牌阵定义
            reader_style: 可选的解读风格
            
        Yields:
            str: 流式返回的文本块
        """
        prompt = self.build_prompt(question, spread_id, cards, custom_spread, reader_style)
        yield from self.llm_service.stream_reading(prompt)

    def get_daily_reading_stream(self, question, cards, reader_style=None):
        """获取每日塔罗流式解读"""
        daily_spread = {
            'name': '每日塔罗',
            'description': '今天的核心能量、机会、挑战与行动提醒',
            'positions': [
                {'name': '今日能量', 'description': '今天最值得留意的核心能量'}
            ]
        }
        daily_question = question or '请为我解读今天的整体能量、机会、挑战和行动建议。'
        yield from self.get_reading_stream(daily_question, 'custom', cards, daily_spread, reader_style)

    def get_followup_stream(self, original_question, spread_id, cards, reading, followup_question,
                            custom_spread=None, reader_style=None):
        """基于已有牌面和解读继续回答追问"""
        base_prompt = self.build_prompt(original_question, spread_id, cards, custom_spread, reader_style)
        followup_prompt = f"""
{base_prompt}

以上是原始牌面上下文。此前已给出的解读如下：
{reading}

用户现在继续追问：
{followup_question}

请只回答这个追问。必须基于同一组牌面延展，不要重新抽牌；如果追问超出牌面能支持的范围，请说明不确定性，并给出可执行建议。
"""
        yield from self.llm_service.stream_reading(followup_prompt)
