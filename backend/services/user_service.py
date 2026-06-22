"""用户认证与云端历史同步服务"""
import json
import os
import sqlite3
from datetime import datetime

from config import Config
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash


def utc_now():
    """返回 SQLite 友好的 UTC 时间字符串"""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


class UserService:
    """轻量级 SQLite 用户服务"""

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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_login TEXT
                )
            """)
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
                    INSERT INTO users (email, password_hash, display_name, created_at, last_login)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (clean_email, generate_password_hash(password), clean_name, now, now)
                )
                user = {
                    'id': cursor.lastrowid,
                    'email': clean_email,
                    'display_name': clean_name
                }
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

    def _public_user(self, row):
        return {
            'id': row['id'],
            'email': row['email'],
            'display_name': row['display_name']
        }
