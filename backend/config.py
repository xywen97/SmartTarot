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
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://localhost:3000').split(',')
    
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
