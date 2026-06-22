"""占卜相关 API"""
from flask import Blueprint, request, jsonify, Response
from services.tarot_service import TarotService
from services.spread_recommender import SpreadRecommender
from services.record_service import RecordService
from data.spreads import get_spread_by_id
from utils.validators import validate_question, sanitize_input
import json

reading_bp = Blueprint('reading', __name__, url_prefix='/api/reading')
tarot_service = TarotService()
spread_recommender = SpreadRecommender()
record_service = RecordService()


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
        custom_spread = data.get('custom_spread')

        cards = tarot_service.draw_cards(spread_id, custom_spread)
        
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
        custom_spread = data.get('custom_spread')
        reader_style = data.get('reader_style')

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

        # 流式 generator 在请求上下文外执行，需提前捕获 request 信息
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        def generate():
            """生成器函数，用于流式返回"""
            reading_parts = []
            try:
                for text in tarot_service.get_reading_stream(
                    question,
                    spread_id,
                    cards,
                    custom_spread=custom_spread,
                    reader_style=reader_style
                ):
                    reading_parts.append(text)
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"

                full_reading = ''.join(reading_parts)
                spread = get_spread_by_id(spread_id)
                record_service.save(
                    record_type='tarot',
                    request_data={
                        'question': question,
                        'spread_id': spread_id,
                        'spread_name': custom_spread.get('name', 'Custom Spread') if custom_spread else (spread.name if spread else spread_id),
                        'spread_name_cn': custom_spread.get('name', '自定义牌阵') if custom_spread else (spread.name_cn if spread else spread_id),
                        'reader_style': reader_style or 'default',
                    },
                    cards=cards,
                    reading=full_reading,
                    endpoint='/api/reading/interpret',
                    client_ip=client_ip,
                    user_agent=user_agent,
                )

                yield f"data: {json.dumps({'type': 'done'})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@reading_bp.route('/daily', methods=['POST'])
def daily_tarot():
    """
    每日塔罗 API（流式）

    Request Body:
        {
            "question": "可选的今日关注点",
            "reader_style": "gentle|direct|psychology|practical"
        }
    """
    try:
        data = request.get_json() or {}
        question = sanitize_input(data.get('question', ''))
        reader_style = data.get('reader_style')
        cards = tarot_service.draw_cards('single')

        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        def generate():
            reading_parts = []
            try:
                yield f"data: {json.dumps({'type': 'cards', 'cards': cards})}\n\n"

                for text in tarot_service.get_daily_reading_stream(question, cards, reader_style):
                    reading_parts.append(text)
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"

                record_service.save(
                    record_type='daily_tarot',
                    request_data={
                        'question': question or '每日塔罗',
                        'spread_id': 'daily',
                        'spread_name': 'Daily Tarot',
                        'spread_name_cn': '每日塔罗',
                        'reader_style': reader_style or 'default',
                    },
                    cards=cards,
                    reading=''.join(reading_parts),
                    endpoint='/api/reading/daily',
                    client_ip=client_ip,
                    user_agent=user_agent,
                )

                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@reading_bp.route('/follow-up', methods=['POST'])
def follow_up():
    """
    基于当前牌面继续追问（流式）
    """
    try:
        data = request.get_json() or {}
        original_question = sanitize_input(data.get('original_question', ''))
        followup_question = sanitize_input(data.get('followup_question', ''))
        spread_id = data.get('spread_id', 'single')
        cards = data.get('cards', [])
        reading = data.get('reading', '')
        custom_spread = data.get('custom_spread')
        reader_style = data.get('reader_style')

        is_valid, error_msg = validate_question(followup_question)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400

        if not original_question or not cards or not reading:
            return jsonify({
                'success': False,
                'error': '缺少原始问题、牌面或解读内容'
            }), 400

        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        def generate():
            answer_parts = []
            try:
                for text in tarot_service.get_followup_stream(
                    original_question,
                    spread_id,
                    cards,
                    reading,
                    followup_question,
                    custom_spread=custom_spread,
                    reader_style=reader_style
                ):
                    answer_parts.append(text)
                    yield f"data: {json.dumps({'type': 'content', 'text': text})}\n\n"

                record_service.save(
                    record_type='tarot_followup',
                    request_data={
                        'original_question': original_question,
                        'followup_question': followup_question,
                        'spread_id': spread_id,
                        'reader_style': reader_style or 'default',
                    },
                    cards=cards,
                    reading=''.join(answer_parts),
                    endpoint='/api/reading/follow-up',
                    client_ip=client_ip,
                    user_agent=user_agent,
                )

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
