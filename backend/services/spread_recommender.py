"""智能牌阵推荐服务"""
from services.llm_service import LLMService

class SpreadRecommender:
    """牌阵推荐器"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def recommend(self, question: str) -> dict:
        """
        根据问题推荐最合适的牌阵
        
        Args:
            question: 用户的问题
            
        Returns:
            {
                'spread_id': 推荐的牌阵ID,
                'reason': 推荐理由,
                'confidence': 置信度 (0-1)
            }
        """
        prompt = f"""你是一位专业的塔罗牌占卜师。根据用户的问题，推荐最合适的牌阵。

可选牌阵：
1. single - 单牌占卜（1张）：适合快速洞察、简单问题、核心能量
2. three_card - 三牌阵（3张）：适合分析过去-现在-未来、事态发展、时间线问题
3. celtic_cross - 凯尔特十字（10张）：适合复杂问题、全面分析、深入探讨
4. relationship - 关系牌阵（5张）：适合亲密关系、人际互动、合作关系问题
5. decision - 决策牌阵（4张）：适合二选一、取舍、风险比较、行动方向
6. monthly - 月度展望（7张）：适合未来一个月的整体规划、事业关系财务综合展望

用户问题：{question}

请分析问题的复杂度、时间维度、需要的洞察深度，然后推荐最合适的牌阵。

请以JSON格式回复，不要包含任何其他文字：
{{
    "spread_id": "推荐的牌阵ID（single/three_card/celtic_cross/relationship/decision/monthly）",
    "reason": "推荐理由（50字以内）",
    "confidence": 置信度（0-1之间的数字）
}}"""

        try:
            # 解析响应
            import json
            result_text = self.llm_service.get_reading(prompt).strip()
            
            # 尝试提取JSON（可能包含额外文字）
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            
            # 验证结果
            valid_spreads = ['single', 'three_card', 'celtic_cross', 'relationship', 'decision', 'monthly']
            if result['spread_id'] not in valid_spreads:
                result['spread_id'] = 'single'  # 默认
            
            return result
            
        except Exception as e:
            print(f"推荐失败: {e}")
            # 返回默认推荐
            return {
                'spread_id': 'single',
                'reason': '为您选择了简单快速的单牌占卜',
                'confidence': 0.5
            }
