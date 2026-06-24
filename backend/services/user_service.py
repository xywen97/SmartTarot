"""用户认证与云端历史同步服务"""
import hmac
import json
import os
import secrets
import sqlite3
import uuid
from datetime import datetime

from config import Config
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash


def utc_now():
    """返回 SQLite 友好的 UTC 时间字符串"""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


class UserService:
    """轻量级 SQLite 用户服务"""

    RECHARGE_PACKAGES = {
        'starter': {
            'id': 'starter',
            'name': '入门补充包',
            'credits': 10,
            'amount_cents': 990,
        },
        'standard': {
            'id': 'standard',
            'name': '标准补充包',
            'credits': 30,
            'amount_cents': 2490,
        },
        'premium': {
            'id': 'premium',
            'name': '高频补充包',
            'credits': 100,
            'amount_cents': 6990,
        },
    }
    PAYMENT_PROVIDERS = {'wechat', 'alipay'}

    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        self._ensure_database()

    def _connect(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_database(self):
        with self._connect() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    query_credits INTEGER NOT NULL DEFAULT {Config.FREE_QUERY_CREDITS},
                    created_at TEXT NOT NULL,
                    last_login TEXT
                )
            """)
            self._ensure_column(conn, 'users', 'query_credits', f'INTEGER NOT NULL DEFAULT {Config.FREE_QUERY_CREDITS}')
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cloud_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    client_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    UNIQUE(user_id, client_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS credit_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    delta INTEGER NOT NULL,
                    balance_after INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    reference_id TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    UNIQUE(user_id, reason, reference_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recharge_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_no TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    package_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    amount_cents INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    qr_code_url TEXT,
                    provider_trade_no TEXT,
                    created_at TEXT NOT NULL,
                    paid_at TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)

    def _ensure_column(self, conn, table, column, definition):
        columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
        if column not in {row['name'] for row in columns}:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def create_user(self, email, password, display_name=None):
        clean_email = email.strip().lower()
        clean_name = (display_name or clean_email.split('@')[0]).strip()[:80]

        if len(password) < 8:
            raise ValueError("密码至少需要 8 个字符")

        now = utc_now()
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO users (email, password_hash, display_name, query_credits, created_at, last_login)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (clean_email, generate_password_hash(password), clean_name, Config.FREE_QUERY_CREDITS, now, now)
                )
                user = {
                    'id': cursor.lastrowid,
                    'email': clean_email,
                    'display_name': clean_name,
                    'query_credits': Config.FREE_QUERY_CREDITS
                }
                self._insert_ledger(
                    conn,
                    user['id'],
                    Config.FREE_QUERY_CREDITS,
                    Config.FREE_QUERY_CREDITS,
                    'signup_bonus',
                    f"user:{user['id']}",
                    {'note': 'initial free query credits'}
                )
        except sqlite3.IntegrityError:
            raise ValueError("该邮箱已注册")

        return user, self.create_token(user['id'])

    def authenticate(self, email, password):
        clean_email = email.strip().lower()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (clean_email,)
            ).fetchone()

            if not row or not check_password_hash(row['password_hash'], password):
                raise ValueError("邮箱或密码错误")

            conn.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (utc_now(), row['id'])
            )

        user = self._public_user(row)
        return user, self.create_token(user['id'])

    def create_token(self, user_id):
        return self.serializer.dumps({'user_id': user_id}, salt='auth-token')

    def verify_token(self, token):
        try:
            data = self.serializer.loads(
                token,
                salt='auth-token',
                max_age=Config.AUTH_TOKEN_MAX_AGE
            )
        except SignatureExpired:
            raise ValueError("登录已过期，请重新登录")
        except BadSignature:
            raise ValueError("无效的登录凭证")

        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?",
                (data['user_id'],)
            ).fetchone()

        if not row:
            raise ValueError("用户不存在")

        return self._public_user(row)

    def sync_readings(self, user_id, readings):
        now = utc_now()
        synced = 0

        with self._connect() as conn:
            for reading in readings:
                client_id = str(reading.get('id', '')).strip()
                if not client_id:
                    continue

                payload = json.dumps(reading, ensure_ascii=False)
                conn.execute(
                    """
                    INSERT INTO cloud_readings (user_id, client_id, payload, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, client_id) DO UPDATE SET
                        payload = excluded.payload,
                        updated_at = excluded.updated_at
                    """,
                    (user_id, client_id, payload, now, now)
                )
                synced += 1

        return synced

    def get_readings(self, user_id):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT payload FROM cloud_readings
                WHERE user_id = ?
                ORDER BY updated_at DESC
                """,
                (user_id,)
            ).fetchall()

        readings = []
        for row in rows:
            try:
                readings.append(json.loads(row['payload']))
            except json.JSONDecodeError:
                continue
        return readings

    def get_credit_status(self, user_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT query_credits FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()

        if not row:
            raise ValueError("用户不存在")

        return {
            'query_credits': row['query_credits'],
            'free_initial_credits': Config.FREE_QUERY_CREDITS,
            'recharge_packages': list(self.RECHARGE_PACKAGES.values())
        }

    def consume_query_credit(self, user_id, *, endpoint, request_summary=None):
        operation_id = uuid.uuid4().hex
        metadata = {
            'endpoint': endpoint,
            'request': request_summary or {}
        }

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.execute(
                """
                UPDATE users
                SET query_credits = query_credits - 1
                WHERE id = ? AND query_credits > 0
                RETURNING query_credits
                """,
                (user_id,)
            )
            row = cursor.fetchone()
            if not row:
                current = conn.execute(
                    "SELECT query_credits FROM users WHERE id = ?",
                    (user_id,)
                ).fetchone()
                if not current:
                    raise ValueError("用户不存在")
                return {
                    'success': False,
                    'error': '可用查询次数不足，请充值后继续使用',
                    'query_credits': current['query_credits']
                }

            balance_after = row['query_credits']
            self._insert_ledger(
                conn,
                user_id,
                -1,
                balance_after,
                'query_consume',
                operation_id,
                metadata
            )

        return {
            'success': True,
            'operation_id': operation_id,
            'query_credits': balance_after
        }

    def refund_query_credit(self, user_id, operation_id, *, reason='query_failed'):
        if not operation_id:
            return self.get_credit_status(user_id)

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            consumed = conn.execute(
                """
                SELECT id FROM credit_ledger
                WHERE user_id = ? AND reason = 'query_consume' AND reference_id = ?
                """,
                (user_id, operation_id)
            ).fetchone()
            refunded = conn.execute(
                """
                SELECT id FROM credit_ledger
                WHERE user_id = ? AND reason = ? AND reference_id = ?
                """,
                (user_id, reason, operation_id)
            ).fetchone()

            if not consumed or refunded:
                row = conn.execute(
                    "SELECT query_credits FROM users WHERE id = ?",
                    (user_id,)
                ).fetchone()
                return {'query_credits': row['query_credits'] if row else 0}

            cursor = conn.execute(
                """
                UPDATE users
                SET query_credits = query_credits + 1
                WHERE id = ?
                RETURNING query_credits
                """,
                (user_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("用户不存在")

            self._insert_ledger(
                conn,
                user_id,
                1,
                row['query_credits'],
                reason,
                operation_id,
                {'note': 'refunded failed query credit'}
            )

        return {'query_credits': row['query_credits']}

    def get_recharge_packages(self):
        return list(self.RECHARGE_PACKAGES.values())

    def create_recharge_order(self, user_id, package_id, provider):
        package = self.RECHARGE_PACKAGES.get(str(package_id or '').strip())
        clean_provider = str(provider or '').strip().lower()

        if not package:
            raise ValueError("无效的充值套餐")
        if clean_provider not in self.PAYMENT_PROVIDERS:
            raise ValueError("无效的支付方式")

        order_no = self._new_order_no(clean_provider)
        now = utc_now()
        qr_code_url = self._placeholder_qr_code_url(order_no, clean_provider)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO recharge_orders (
                    order_no, user_id, package_id, provider, credits, amount_cents,
                    status, qr_code_url, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?)
                """,
                (
                    order_no,
                    user_id,
                    package['id'],
                    clean_provider,
                    package['credits'],
                    package['amount_cents'],
                    qr_code_url,
                    now
                )
            )

        return self.get_recharge_order(user_id, order_no)

    def get_recharge_order(self, user_id, order_no):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM recharge_orders
                WHERE user_id = ? AND order_no = ?
                """,
                (user_id, order_no)
            ).fetchone()

        if not row:
            raise ValueError("充值订单不存在")
        return self._public_recharge_order(row)

    def mark_recharge_paid(self, order_no, provider, provider_trade_no='', signature=''):
        if not self._verify_payment_signature(order_no, provider, provider_trade_no, signature):
            raise ValueError("支付回调签名验证失败")

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            order = conn.execute(
                "SELECT * FROM recharge_orders WHERE order_no = ?",
                (order_no,)
            ).fetchone()

            if not order:
                raise ValueError("充值订单不存在")
            if order['provider'] != provider:
                raise ValueError("支付方式不匹配")

            if order['status'] == 'paid':
                return self._public_recharge_order(order)
            if order['status'] != 'pending':
                raise ValueError("订单状态不允许入账")

            now = utc_now()
            cursor = conn.execute(
                """
                UPDATE users
                SET query_credits = query_credits + ?
                WHERE id = ?
                RETURNING query_credits
                """,
                (order['credits'], order['user_id'])
            )
            balance = cursor.fetchone()['query_credits']

            conn.execute(
                """
                UPDATE recharge_orders
                SET status = 'paid', paid_at = ?, provider_trade_no = ?
                WHERE id = ?
                """,
                (now, provider_trade_no, order['id'])
            )
            self._insert_ledger(
                conn,
                order['user_id'],
                order['credits'],
                balance,
                'recharge_paid',
                order['order_no'],
                {
                    'provider': provider,
                    'package_id': order['package_id'],
                    'amount_cents': order['amount_cents']
                }
            )

            updated = conn.execute(
                "SELECT * FROM recharge_orders WHERE id = ?",
                (order['id'],)
            ).fetchone()

        return self._public_recharge_order(updated)

    def _insert_ledger(self, conn, user_id, delta, balance_after, reason, reference_id, metadata=None):
        conn.execute(
            """
            INSERT INTO credit_ledger (
                user_id, delta, balance_after, reason, reference_id, metadata, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                delta,
                balance_after,
                reason,
                reference_id,
                json.dumps(metadata or {}, ensure_ascii=False),
                utc_now()
            )
        )

    def _public_user(self, row):
        return {
            'id': row['id'],
            'email': row['email'],
            'display_name': row['display_name'],
            'query_credits': row['query_credits']
        }

    def _public_recharge_order(self, row):
        return {
            'order_no': row['order_no'],
            'package_id': row['package_id'],
            'provider': row['provider'],
            'credits': row['credits'],
            'amount_cents': row['amount_cents'],
            'amount': row['amount_cents'] / 100,
            'status': row['status'],
            'qr_code_url': row['qr_code_url'],
            'provider_trade_no': row['provider_trade_no'],
            'created_at': row['created_at'],
            'paid_at': row['paid_at']
        }

    def _new_order_no(self, provider):
        return f"{provider}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(6)}"

    def _placeholder_qr_code_url(self, order_no, provider):
        filenames = {
            'wechat': 'wechat.png',
            'alipay': 'alipay.png',
        }
        return f"/assets/{filenames[provider]}"

    def _verify_payment_signature(self, order_no, provider, provider_trade_no, signature):
        if not Config.PAYMENT_NOTIFY_SECRET:
            return False

        message = f"{order_no}|{provider}|{provider_trade_no}".encode('utf-8')
        digest = hmac.new(
            Config.PAYMENT_NOTIFY_SECRET.encode('utf-8'),
            message,
            'sha256'
        ).hexdigest()
        return hmac.compare_digest(digest, signature or '')
