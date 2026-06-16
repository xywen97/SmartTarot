"""占卜记录持久化服务 — 每次请求保存为一个 JSON 文件"""
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from config import Config


class RecordService:
    """将占卜请求与结果写入 records/ 目录，一次请求一个文件"""

    def __init__(self):
        self.enabled = Config.RECORDS_ENABLED
        self.records_dir = Config.RECORDS_DIR
        if self.enabled:
            os.makedirs(self.records_dir, exist_ok=True)

    def save(
        self,
        *,
        record_type: str,
        request_data: dict,
        reading: str,
        cards: Optional[list] = None,
        endpoint: str = '',
        extra: Optional[dict] = None,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[str]:
        """
        保存一条占卜记录

        Returns:
            保存的文件路径，未启用或失败时返回 None
        """
        if not self.enabled:
            return None

        now = datetime.now(timezone.utc).astimezone()
        record_id = f"{now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        record = {
            'id': record_id,
            'timestamp': now.isoformat(),
            'type': record_type,
            'request': request_data,
            'cards': cards or [],
            'reading': reading,
            'meta': {
                'endpoint': endpoint,
                'model': Config.MODEL,
                'client_ip': client_ip,
                'user_agent': user_agent,
                **(extra or {}),
            },
        }

        filename = f"{record_id}.json"
        filepath = os.path.join(self.records_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            print(f"📝 记录已保存: {filepath}")
            return filepath
        except OSError as e:
            print(f"⚠️ 记录保存失败: {e}")
            return None
