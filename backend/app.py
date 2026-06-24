"""Flask 应用主入口"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from api.reading import reading_bp
from api.data import data_bp
from api.divination import divination_bp
from api.auth import auth_bp
from api.billing import billing_bp


def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 启用 CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(reading_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(divination_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(billing_bp)
    
    # 健康检查端点
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'Tarot API is running'
        })
    
    # 根路径
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'name': 'Tarot AI API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'draw': '/api/reading/draw',
                'interpret': '/api/reading/interpret',
                'deck': '/api/data/deck',
                'spreads': '/api/data/spreads',
                'auth': '/api/auth/login',
                'billing': '/api/billing/status'
            }
        })
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 'API endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app


if __name__ == '__main__':
    # 验证配置
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        exit(1)
    
    # 创建应用
    app = create_app()
    
    # 启动服务器
    print("🌙 启动 Tarot AI 后端服务...")
    print(f"📍 API 地址: http://localhost:5001")
    print(f"🔑 使用模型: {Config.MODEL}")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=Config.DEBUG
    )
