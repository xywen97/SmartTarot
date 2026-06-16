"""周公解梦占卜实现"""
from services.divination_factory import BaseDivination
from services.llm_service import LLMService
from typing import Generator


class DreamDivination(BaseDivination):
    """周公解梦占卜"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def get_name(self) -> str:
        return "周公解梦"
    
    def get_description(self) -> str:
        return "解析梦境含义，探索潜意识的信息"
    
    def validate_input(self, data: dict) -> tuple[bool, str]:
        """验证输入"""
        dream = data.get('dream', '').strip()
        if not dream:
            return False, "请描述你的梦境"
        
        if len(dream) < 10:
            return False, "梦境描述太简短，请提供更多细节"
        
        return True, ""
    
    def perform_divination(self, data: dict) -> Generator[str, None, None]:
        """执行周公解梦"""
        dream = data['dream']
        emotion = data.get('emotion', '').strip()
        context = data.get('context', '').strip()
        
        prompt = f"""你是一位精通周公解梦和梦境心理学的专家，请解析以下梦境：

梦境描述：
{dream}

{f'梦中情绪：{emotion}' if emotion else ''}
{f'现实背景：{context}' if context else ''}

请提供深入的梦境解析，包括：

1. **梦境象征分析**
   - 梦中关键元素的象征意义
   - 传统周公解梦的解释

2. **心理学解读**
   - 从心理学角度分析潜意识信息
   - 可能反映的内心状态

3. **情绪与情感**
   - 梦境中的情感线索
   - 压抑或未表达的情感

4. **现实映射**
   - 梦境可能与现实的关联
   - 需要关注的现实问题

5. **预示与启示**
   - 梦境的预示意义（如有）
   - 给你的启示和建议

6. **建议与指导**
   - 如何应对梦境传达的信息
   - 自我成长的方向

请用温和、富有洞察力的语气，帮助解梦者理解潜意识的信息。"""

        # 流式生成
        for text in self.llm_service.generate_stream(prompt):
            yield text
