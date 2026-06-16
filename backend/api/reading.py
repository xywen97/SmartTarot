"""占卜相关 API"""
from flask import Blueprint, request, jsonify, Response
from services.tarot_service import TarotService
from services.spread_recommender import SpreadRecommender
from utils.validators import validate_question, sanitize_input
import json

reading_bp = Blueprint('reading', __name__, url_prefix='/api/reading')
tarot_service = TarotService()
spread_recommender = SpreadRecommender()


@reading_bp.route('/draw', methods=['POST'])
def draw_cards():
    """
    抽牌 API
    
    Request Body:
        {
            "spread_id": "single"
        }
    
    Response:
        {
            "cards": [...]
        }
    """
    try:
        data = request.get_json()
        spread_id = data.get('spread_id', 'single')
        
        cards = tarot_service.draw_cards(spread_id)
        
        return jsonify({
            'success': True,
            'cards': cards
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@reading_bp.route('/interpret', methods=['POST'])
def interpret_cards():
    """
    获取解读 API（流式）
    
    Request Body:
        {
            "question": "我的事业发展如何？",
            "spread_id": "single",
            "cards": [...]
        }
    
    Response:
        Server-Sent Events (text/event-stream)
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        spread_id = data.get('spread_id', 'single')
        cards = data.get('cards', [])

        # 清理输入
        question = sanitize_input(question)

        # 验证问题
        is_valid, error_msg = validate_question(question)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400

        if not cards:
            return jsonify({
                'success': False,
                'error': '未提供卡牌信息'
            }), 400
        
        def generate():
            """生成器函数，用于流式返回"""
            try:
                for text in tarot_service.get_reading_stream(question, spread_id, cards):
                    # 使用 SSE 格式
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"
                
                # 发送完成信号
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@reading_bp.route('/recommend-spread', methods=['POST'])
def recommend_spread():
    """
    智能推荐牌阵 API
    
    Request Body:
        {
            "question": "用户的问题"
        }
    
    Response:
        {
            "spread_id": "single",
            "reason": "推荐理由",
            "confidence": 0.85
        }
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        # 清理和验证输入
        question = sanitize_input(question)
        is_valid, error_msg = validate_question(question)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # 获取推荐
        recommendation = spread_recommender.recommend(question)
        
        return jsonify({
            'success': True,
            **recommendation
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
