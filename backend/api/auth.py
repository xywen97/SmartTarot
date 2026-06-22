"""认证与云同步 API"""
from functools import wraps

from flask import Blueprint, jsonify, request

from services.user_service import UserService


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
user_service = UserService()


def get_bearer_token():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return ''
    return auth_header.split(' ', 1)[1].strip()


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({
                'success': False,
                'error': '请先登录'
            }), 401

        try:
            request.current_user = user_service.verify_token(token)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 401

        return fn(*args, **kwargs)

    return wrapper


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json() or {}
        user, token = user_service.create_user(
            email=data.get('email', ''),
            password=data.get('password', ''),
            display_name=data.get('display_name')
        )
        return jsonify({
            'success': True,
            'user': user,
            'token': token
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        user, token = user_service.authenticate(
            email=data.get('email', ''),
            password=data.get('password', '')
        )
        return jsonify({
            'success': True,
            'user': user,
            'token': token
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 401


@auth_bp.route('/me', methods=['GET'])
@require_auth
def me():
    return jsonify({
        'success': True,
        'user': request.current_user
    })


@auth_bp.route('/sync', methods=['POST'])
@require_auth
def sync_readings():
    data = request.get_json() or {}
    readings = data.get('readings', [])

    if not isinstance(readings, list):
        return jsonify({
            'success': False,
            'error': 'readings 必须是数组'
        }), 400

    synced = user_service.sync_readings(request.current_user['id'], readings)
    cloud_readings = user_service.get_readings(request.current_user['id'])

    return jsonify({
        'success': True,
        'synced': synced,
        'readings': cloud_readings
    })


@auth_bp.route('/readings', methods=['GET'])
@require_auth
def get_readings():
    return jsonify({
        'success': True,
        'readings': user_service.get_readings(request.current_user['id'])
    })
