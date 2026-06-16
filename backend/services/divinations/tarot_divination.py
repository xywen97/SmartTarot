"""塔罗牌占卜实现"""
from services.divination_factory import BaseDivination
from services.tarot_service import TarotService
from typing import Generator


class TarotDivination(BaseDivination):
    """塔罗牌占卜"""
    
    def __init__(self):
        self.tarot_service = TarotService()
    
    def get_name(self) -> str:
        return "塔罗占卜"
    
    def get_description(self) -> str:
        return "使用78张塔罗牌进行占卜，洞察过去、现在和未来"
    
    def validate_input(self, data: dict) -> tuple[bool, str]:
        """验证输入"""
        question = data.get('question', '').strip()
        if not question:
            return False, "请输入问题"
        
        spread_id = data.get('spread_id', 'single')
        valid_spreads = ['single', 'three_card', 'celtic_cross']
        if spread_id not in valid_spreads:
            return False, f"无效的牌阵: {spread_id}"
        
        return True, ""
    
    def perform_divination(self, data: dict) -> Generator[str, None, None]:
        """执行塔罗占卜"""
        question = data['question']
        spread_id = data.get('spread_id', 'single')
        
        # 抽牌
        cards = self.tarot_service.draw_cards(spread_id)
        
        # 流式解读
        for text in self.tarot_service.get_reading_stream(question, spread_id, cards):
            yield text
