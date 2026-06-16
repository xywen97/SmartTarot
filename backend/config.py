"""配置管理"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置"""
    
    # API 配置
    API_KEY = os.getenv('POLOAI_API_KEY', '')
    API_BASE_URL = os.getenv('POLOAI_BASE_URL', 'https://poloai.top')
    MODEL = os.getenv('MODEL', 'claude-opus-4-8')
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS 配置
    # - 未设置且 DEBUG=True：允许所有来源（clone 即用，无需写 IP）
    # - 设为 *：允许所有来源
    # - 其他：逗号分隔的明确域名列表（生产环境推荐）
    _cors_env = os.getenv('CORS_ORIGINS', '').strip()
    if _cors_env == '*':
        CORS_ORIGINS = ['*']
    elif _cors_env:
        CORS_ORIGINS = [o.strip() for o in _cors_env.split(',') if o.strip()]
    elif DEBUG:
        CORS_ORIGINS = ['*']
    else:
        CORS_ORIGINS = ['http://localhost:8080', 'http://localhost:3000']
    
    # LLM 配置
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4096'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    @classmethod
    def validate(cls):
        """验证必需的配置"""
        if not cls.API_KEY:
            raise ValueError("POLOAI_API_KEY 环境变量未设置")
        if not cls.API_BASE_URL:
            raise ValueError("POLOAI_BASE_URL 环境变量未设置")
        return True
