"""查询余量与充值 API"""
from flask import Blueprint, jsonify, request

from api.auth import require_auth
from services.user_service import UserService


billing_bp = Blueprint('billing', __name__, url_prefix='/api/billing')
user_service = UserService()


@billing_bp.route('/status', methods=['GET'])
@require_auth
def get_status():
    return jsonify({
        'success': True,
        **user_service.get_credit_status(request.current_user['id'])
    })


@billing_bp.route('/packages', methods=['GET'])
@require_auth
def get_packages():
    return jsonify({
        'success': True,
        'packages': user_service.get_recharge_packages()
    })


@billing_bp.route('/recharge/orders', methods=['POST'])
@require_auth
def create_recharge_order():
    try:
        data = request.get_json() or {}
        order = user_service.create_recharge_order(
            request.current_user['id'],
            data.get('package_id'),
            data.get('provider')
        )
        return jsonify({
            'success': True,
            'order': order,
            'message': '订单已创建。请接入微信/支付宝扫码下单接口替换占位二维码。'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@billing_bp.route('/recharge/orders/<order_no>', methods=['GET'])
@require_auth
def get_recharge_order(order_no):
    try:
        return jsonify({
            'success': True,
            'order': user_service.get_recharge_order(request.current_user['id'], order_no)
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@billing_bp.route('/recharge/notify', methods=['POST'])
def recharge_notify():
    """
    预留支付服务端回调入口。
    真实接入时应由微信/支付宝服务端调用，并使用 PAYMENT_NOTIFY_SECRET 校验签名。
    """
    try:
        data = request.get_json() or {}
        order = user_service.mark_recharge_paid(
            order_no=str(data.get('order_no', '')).strip(),
            provider=str(data.get('provider', '')).strip().lower(),
            provider_trade_no=str(data.get('provider_trade_no', '')).strip(),
            signature=str(data.get('signature', '')).strip()
        )
        return jsonify({
            'success': True,
            'order': order
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
