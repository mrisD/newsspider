import json
from base64 import b64decode
from typing import Any

from scrapy import Spider
from scrapy.crawler import Crawler, logger
from newsuniversal_spider.spider_kit.replace import Replacer

class BaseSpider(Spider):
    config: dict[str, Any] | None = None
    text_replacer = Replacer()
    def __init__(self, **kwargs: dict[str, Any]):
        super().__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any):
        spider = super().from_crawler(crawler, *args, **kwargs)

        site_forum_id = kwargs.get("site_forum_id")
        cmdline_config = kwargs.get("config")
        # 从命令行参数中获取base64编码的config，用于解决命令行参数中无法传递json的问题
        cmdline_b64config = kwargs.get("b64config")

        # 如果有命令行参数，则使用命令行参数中的config
        if cmdline_config:
            config = (
                json.loads(cmdline_config)
                if isinstance(cmdline_config, str)
                else cmdline_config
            )
            logger.warning(f"使用命令行中的config: {config}")
        else :
            config = json.loads(b64decode(cmdline_b64config.encode()).decode())
            logger.warning(f"使用命令行中的b64config: {config}")


        if not config:
            raise

    def replace_api_payload(
        self, payload: dict[str, Any] | str, **kwargs
    ) -> dict[str, Any] | str:
        """
        替换API请求参数, 将其中的占位符替换为实际值
        :param payload:
        :param kwargs:
        :return:
        """
        payload = self.text_replacer.replace(payload)
        return payload
    def send_next_request(self, next_stage, stages, item, url=None, **kwargs):
        """
        发送下一步骤请求
        :param next_stage:
        :param item:
        :param stages:
        :param url:
        :return:
        """
        request_func = self.process_func.get(
            f"{next_stage['grab_method']}_{next_stage['type']}"
        )
        if not request_func:
            logger.error(
                f"没有找到对应的请求函数，stage: {next_stage['grab_method']}_{next_stage['type']}"  # noqa E501
            )
            return
        if url:
            return request_func(url, stages, next_stage, **{"item": item}, **kwargs)
        else:
            logger.error(f"item中没有url字段，无法进行下一步骤请求，item: {item}")
