"""LLM 调用服务（OpenAI-compatible Chat Completions）"""
import json
from urllib.parse import urljoin

import requests

from config import Config


class LLMService:
    """OpenAI-compatible LLM 服务类"""

    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.API_BASE_URL.rstrip('/')
        self.chat_completions_url = self._build_chat_completions_url()
        self.model = Config.MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE

    def _build_chat_completions_url(self):
        """允许配置根地址或完整 /chat/completions 地址。"""
        if self.base_url.endswith('/chat/completions'):
            return self.base_url
        if self.base_url.endswith('/v1'):
            return f"{self.base_url}/chat/completions"
        return urljoin(f"{self.base_url}/", "chat/completions")

    def _headers(self, stream=False):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if stream:
            headers["Accept"] = "text/event-stream"
        return headers

    def _payload(self, prompt, stream=False, max_tokens=None):
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": self.temperature,
            "stream": stream,
        }

    def stream_reading(self, prompt):
        """
        流式获取解读。

        Yields:
            str: OpenAI-compatible SSE 的 delta.content 文本块
        """
        try:
            with requests.post(
                self.chat_completions_url,
                headers=self._headers(stream=True),
                json=self._payload(prompt, stream=True),
                stream=True,
                timeout=(10, 300),
            ) as response:
                response.raise_for_status()

                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue

                    line = raw_line.strip()
                    if line.startswith("data:"):
                        line = line[5:].strip()

                    if not line or line == "[DONE]":
                        continue

                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if chunk.get("error"):
                        raise Exception(chunk["error"].get("message") or str(chunk["error"]))

                    for choice in chunk.get("choices", []):
                        delta = choice.get("delta") or {}
                        content = delta.get("content")
                        if content:
                            yield content

                        message = choice.get("message") or {}
                        content = message.get("content")
                        if content:
                            yield content
        except requests.HTTPError as e:
            detail = e.response.text if e.response is not None else str(e)
            raise Exception(f"LLM 调用失败: HTTP {e.response.status_code if e.response else ''} {detail}")
        except Exception as e:
            raise Exception(f"LLM 调用失败: {str(e)}")

    def generate_stream(self, prompt):
        """兼容其他占卜模块的旧方法名。"""
        yield from self.stream_reading(prompt)

    def get_reading(self, prompt):
        """非流式获取解读（用于测试和推荐器）。"""
        try:
            response = requests.post(
                self.chat_completions_url,
                headers=self._headers(),
                json=self._payload(prompt, stream=False),
                timeout=(10, 120),
            )
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                raise Exception(data["error"].get("message") or str(data["error"]))

            choices = data.get("choices") or []
            if not choices:
                raise Exception("LLM 返回为空")

            message = choices[0].get("message") or {}
            content = message.get("content")
            if content is None:
                raise Exception("LLM 返回缺少 message.content")
            return content
        except requests.HTTPError as e:
            detail = e.response.text if e.response is not None else str(e)
            raise Exception(f"LLM 调用失败: HTTP {e.response.status_code if e.response else ''} {detail}")
        except Exception as e:
            raise Exception(f"LLM 调用失败: {str(e)}")
