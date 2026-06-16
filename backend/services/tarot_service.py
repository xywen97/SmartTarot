"""塔罗牌业务逻辑服务"""
import os
from data.tarot_deck import get_card_by_id, get_deck_size
from data.spreads import get_spread_by_id
from data.tarot_skills import apply_skill_to_reading, TAROT_SKILLS
from services.random_service import RandomService
from services.llm_service import LLMService


class TarotService:
    """塔罗牌服务类"""
    
    def __init__(self):
        self.random_service = RandomService()
        self.llm_service = LLMService()
        self.prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'prompts')
    
    def draw_cards(self, spread_id):
        """
        抽牌
        
        Args:
            spread_id: 牌阵 ID
            
        Returns:
            list: 抽取的牌信息列表
        """
        spread = get_spread_by_id(spread_id)
        if not spread:
            raise ValueError(f"无效的牌阵 ID: {spread_id}")
        
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
    
    def build_prompt(self, question, spread_id, cards):
        """
        构建 Prompt
        
        Args:
            question: 用户问题
            spread_id: 牌阵 ID
            cards: 抽取的牌列表
            
        Returns:
            str: 完整的 Prompt
        """
        spread = get_spread_by_id(spread_id)
        if not spread:
            raise ValueError(f"无效的牌阵 ID: {spread_id}")
        
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
    
    def get_reading_stream(self, question, spread_id, cards):
        """
        获取流式解读
        
        Args:
            question: 用户问题
            spread_id: 牌阵 ID
            cards: 抽取的牌列表
            
        Yields:
            str: 流式返回的文本块
        """
        prompt = self.build_prompt(question, spread_id, cards)
        yield from self.llm_service.stream_reading(prompt)
