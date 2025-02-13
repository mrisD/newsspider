from scrapy import Request

from newsuniversal_spider.spider_kit.fingerprint import request_fingerprint

# 创建一个Request对象
request = Request(
    url="https://example1.com",
    method="GET",
    meta={"current_stage": 1, "fingerprint_meta": "abc"},
    cb_kwargs={"item": {"url": "https://example.com/item", "title": "Example Item"}},
)

# 生成指纹
fingerprint = request_fingerprint(request)
print("请求指纹:", fingerprint)