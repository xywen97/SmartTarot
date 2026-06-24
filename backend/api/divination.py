"""统一占卜 API"""
from flask import Blueprint, request, jsonify, Response
from api.auth import require_auth
from services.divination_factory import DivinationFactory
from services.record_service import RecordService
from services.user_service import UserService
from utils.validators import sanitize_input
import json

divination_bp = Blueprint('divination', __name__, url_prefix='/api/divination')
record_service = RecordService()
user_service = UserService()


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
@require_auth
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

        usage = user_service.consume_query_credit(
            request.current_user['id'],
            endpoint='/api/divination/perform',
            request_summary={
                'type': divination_type,
                'field_count': len(data)
            }
        )
        if not usage['success']:
            return jsonify({
                'success': False,
                'error': usage['error'],
                'query_credits': usage['query_credits'],
                'recharge_required': True
            }), 402

        user_id = request.current_user['id']
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        # 执行占卜（流式返回）
        def generate():
            reading_parts = []
            try:
                yield f"data: {json.dumps({'type': 'balance', 'query_credits': usage['query_credits']})}\n\n"

                for text in divination.perform_divination(data):
                    reading_parts.append(text)
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"

                record_service.save(
                    record_type=divination_type,
                    request_data=data,
                    reading=''.join(reading_parts),
                    endpoint='/api/divination/perform',
                    client_ip=client_ip,
                    user_agent=user_agent,
                )

                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                credit_status = user_service.refund_query_credit(user_id, usage['operation_id'])
                yield f"data: {json.dumps({'type': 'balance', 'query_credits': credit_status['query_credits']})}\n\n"
                yield f"data: {json.dumps({'type': 'error', 'error': str(e), 'query_credits': credit_status['query_credits']})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
