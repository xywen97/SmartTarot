"""统一占卜 API"""
from flask import Blueprint, request, jsonify, Response
from services.divination_factory import DivinationFactory
from utils.validators import sanitize_input
import json

divination_bp = Blueprint('divination', __name__, url_prefix='/api/divination')


@divination_bp.route('/types', methods=['GET'])
def get_divination_types():
    """
    获取所有占卜方式
    
    Response:
        {
            "types": [
                {
                    "type": "tarot",
                    "name": "塔罗占卜",
                    "description": "..."
                },
                ...
            ]
        }
    """
    try:
        types = DivinationFactory.get_all_types()
        return jsonify({
            'success': True,
            'types': types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@divination_bp.route('/perform', methods=['POST'])
def perform_divination():
    """
    执行占卜（统一接口）
    
    Request Body:
        {
            "type": "tarot|birthday|dream",
            "data": {
                // 根据不同type传入不同数据
            }
        }
    
    Response:
        流式返回占卜结果
    """
    try:
        body = request.get_json()
        divination_type = body.get('type', 'tarot')
        data = body.get('data', {})
        
        # 清理输入
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = sanitize_input(value)
        
        # 获取占卜实例
        divination = DivinationFactory.get_divination(divination_type)
        
        # 验证输入
        is_valid, error_msg = divination.validate_input(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # 执行占卜（流式返回）
        def generate():
            try:
                for text in divination.perform_divination(data):
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"
                
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
