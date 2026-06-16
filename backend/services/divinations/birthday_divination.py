"""生辰八字占卜实现"""
from services.divination_factory import BaseDivination
from services.llm_service import LLMService
from typing import Generator
from datetime import datetime


class BirthdayDivination(BaseDivination):
    """生辰八字占卜"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def get_name(self) -> str:
        return "生辰八字"
    
    def get_description(self) -> str:
        return "根据出生年月日时分析五行八字，预测运势"
    
    def validate_input(self, data: dict) -> tuple[bool, str]:
        """验证输入"""
        birth_date = data.get('birth_date', '').strip()
        if not birth_date:
            return False, "请输入出生日期"
        
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            return False, "日期格式错误，请使用 YYYY-MM-DD 格式"
        
        birth_time = data.get('birth_time', '').strip()
        if birth_time:
            try:
                datetime.strptime(birth_time, '%H:%M')
            except ValueError:
                return False, "时间格式错误，请使用 HH:MM 格式"
        
        return True, ""
    
    def perform_divination(self, data: dict) -> Generator[str, None, None]:
        """执行生辰八字占卜"""
        birth_date = data['birth_date']
        birth_time = data.get('birth_time', '12:00')
        gender = data.get('gender', '未知')
        question = data.get('question', '整体运势')
        
        prompt = f"""你是一位精通中国传统命理学的大师，请根据以下信息进行生辰八字分析：

出生日期：{birth_date}
出生时间：{birth_time}（若不确定，按正午时分析）
性别：{gender}
关注问题：{question}

请提供详细的八字分析，包括：

1. **五行分析**
   - 分析此人的五行属性（金木水火土）
   - 五行强弱与平衡状况

2. **性格特征**
   - 基于八字推断的性格特点
   - 天赋与潜力

3. **运势分析**
   - 事业运势
   - 财运分析
   - 感情姻缘
   - 健康状况

4. **流年运势**
   - 当前年份的运势走向
   - 需要注意的事项

5. **建议与指导**
   - 开运建议
   - 需要注意的方面

请用温和、专业的语气，给出富有洞察力的分析。"""

        # 流式生成
        for text in self.llm_service.generate_stream(prompt):
            yield text
