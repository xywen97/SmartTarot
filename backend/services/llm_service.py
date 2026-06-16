"""LLM 调用服务"""
from anthropic import Anthropic
from config import Config


class LLMService:
    """LLM 服务类"""
    
    def __init__(self):
        """初始化 Anthropic 客户端"""
        self.client = Anthropic(
            api_key=Config.API_KEY,
            base_url=Config.API_BASE_URL
        )
        self.model = Config.MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def stream_reading(self, prompt):
        """
        流式获取解读
        
        Args:
            prompt: 完整的 prompt 文本
            
        Yields:
            str: 流式返回的文本块
        """
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"LLM 调用失败: {str(e)}")
    
    def get_reading(self, prompt):
        """
        非流式获取解读（用于测试）
        
        Args:
            prompt: 完整的 prompt 文本
            
        Returns:
            str: 完整的解读文本
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"LLM 调用失败: {str(e)}")
