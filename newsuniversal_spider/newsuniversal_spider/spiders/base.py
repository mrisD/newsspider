import json
from base64 import b64decode
from typing import Any

from scrapy import Spider
from scrapy.crawler import Crawler, logger


class BaseSpider(Spider):
    config: dict[str, Any] | None = None
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
        # spider.config = config
        # spider.site_forum_id = site_forum_id
        #
        # # 将config中的custom_settings设置到spider中
        # custom_settings = spider.config.get("custom_settings")
        # if custom_settings:
        #     settings = (
        #         json.loads(custom_settings)
        #         if isinstance(custom_settings, str)
        #         else custom_settings
        #     )
        #
        #     if settings.get("playwright_cdp_url"):
        #         settings["playwright_cdp_url"] = settings["playwright_cdp_url"].replace(
        #             "crawlab-ubuntu20-desktop", env["CDP_BROWSER_ADDRESS"]
        #         )
        #
        #     # 确保settings中的key都是大写, scrapy中的settings都是大写的
        #     settings = {key.upper(): value for key, value in settings.items()}
        #     spider.settings.setdict(settings, priority="spider")
        #
        # cls.storage.close()
        # return spider
