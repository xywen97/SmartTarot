#!/usr/bin/env python3
"""启动脚本"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.config import Config

if __name__ == '__main__':
    try:
        # 验证配置
        Config.validate()
        print("✅ 配置验证通过")
        
        # 创建应用
        app = create_app()
        
        # 启动服务器
        print("\n🌙 启动 Tarot AI 后端服务...")
        print(f"📍 API 地址: http://localhost:5001")
        print(f"🔑 使用模型: {Config.MODEL}")
        print(f"🌐 CORS 允许源: {', '.join(Config.CORS_ORIGINS)}")
        print("\n按 Ctrl+C 停止服务\n")
        
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=Config.DEBUG
        )
    
    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n请检查 .env 文件，确保所有必需的环境变量已设置。")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)
