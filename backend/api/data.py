"""数据相关 API"""
from flask import Blueprint, jsonify
from data.tarot_deck import get_all_cards
from data.spreads import get_all_spreads

data_bp = Blueprint('data', __name__, url_prefix='/api/data')


@data_bp.route('/deck', methods=['GET'])
def get_deck():
    """
    获取塔罗牌库
    
    Response:
        {
            "cards": [...]
        }
    """
    try:
        cards = get_all_cards()
        return jsonify({
            'success': True,
            'cards': cards
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@data_bp.route('/spreads', methods=['GET'])
def get_spreads():
    """
    获取牌阵列表
    
    Response:
        {
            "spreads": {...}
        }
    """
    try:
        spreads = get_all_spreads()
        return jsonify({
            'success': True,
            'spreads': spreads
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
