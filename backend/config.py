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
    MODEL = os.getenv('MODEL', 'deepseek-v4-pro')
    
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
        CORS_ORIGINS = [
            'http://localhost:8080',
            'http://localhost:8081',
            'http://localhost:3000',
            'http://127.0.0.1:8080',
            'http://127.0.0.1:8081',
            'http://127.0.0.1:3000',
        ]
    
    # LLM 配置
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4096'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

    # 记录配置
    RECORDS_ENABLED = os.getenv('RECORDS_ENABLED', 'True').lower() == 'true'
    RECORDS_DIR = os.getenv(
        'RECORDS_DIR',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'records'))
    )
    ASSETS_DIR = os.getenv(
        'ASSETS_DIR',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
    )

    # 用户与云同步配置
    DATABASE_PATH = os.getenv(
        'DATABASE_PATH',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'tarot.db'))
    )
    AUTH_TOKEN_MAX_AGE = int(os.getenv('AUTH_TOKEN_MAX_AGE', str(7 * 24 * 60 * 60)))
    FREE_QUERY_CREDITS = int(os.getenv('FREE_QUERY_CREDITS', '3'))

    # 支付回调签名配置。未接入真实微信/支付宝前保持为空，回调接口会拒绝入账。
    PAYMENT_NOTIFY_SECRET = os.getenv('PAYMENT_NOTIFY_SECRET', '').strip()
    
    @classmethod
    def validate(cls):
        """验证必需的配置"""
        if not cls.API_KEY:
            raise ValueError("POLOAI_API_KEY 环境变量未设置")
        if not cls.API_BASE_URL:
            raise ValueError("POLOAI_BASE_URL 环境变量未设置")
        if not cls.DEBUG and cls.SECRET_KEY == 'your-secret-key-here':
            raise ValueError("生产环境必须设置安全的 SECRET_KEY")
        return True
