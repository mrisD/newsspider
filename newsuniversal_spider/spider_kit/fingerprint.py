import hashlib
import json
from typing import Optional, Dict, Any

from scrapy import Request
from w3lib.url import canonicalize_url


def request_fingerprint(request: Request) -> str:
    """
    获取request的fingerprint
    :param request: Scrapy的Request对象
    :return: 请求的唯一指纹（SHA-224哈希值）
    """

    def meta_fingerprint() -> Dict[str, Any]:
        """
        获取meta的fingerprint
        :return: 包含meta字段的字典
        """
        meta = request.meta or {}
        return {
            "current_stage": meta.get("current，，_stage"),
            "fingerprint_meta": meta.get("fingerprint_meta"),
        }

    def cb_kwargs_fingerprint() -> Dict[str, Any]:
        """
        获取cb_kwargs的fingerprint
        :return: 包含cb_kwargs字段的字典
        """
        cb_kwargs = request.cb_kwargs or {}
        item = cb_kwargs.get("item", {})
        return {
            "item_url": canonicalize_url(item.get("url"), keep_fragments=True)
            if item.get("url")
            else "",
            "title": item.get("title"),
            "fingerprint_key": item.get("fingerprint_key"),
        }

    try:
        # 构建指纹数据
        fingerprint_data = {
            "url": canonicalize_url(request.url, keep_fragments=True),
            "method": request.method,
            "body": (request.body or b"").hex(),
            **meta_fingerprint(),
            **cb_kwargs_fingerprint(),
        }

        # 生成指纹
        fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha224(fingerprint_json.encode()).hexdigest()
    except Exception as e:
        # 异常处理
        raise ValueError(f"生成指纹失败: {e}")