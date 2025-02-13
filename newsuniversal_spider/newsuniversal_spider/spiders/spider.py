from typing import Any, Callable, Generator

import pkg_resources
from loguru import logger
from scrapy import Request

from newsuniversal_spider.newsuniversal_spider.spiders.detail import (
    ApiDetailSpider,

    HtmlDetailSpider,
)
from newsuniversal_spider.newsuniversal_spider.spiders.list import (
    ApiListSpider,

    HtmlListSpider,
)



def get_installed_packages():
    installed_packages = pkg_resources.working_set
    packages = {pkg.project_name: pkg.version for pkg in installed_packages}
    return packages


class UniversalSpider(

    HtmlListSpider,
    HtmlDetailSpider,

    ApiListSpider,
    ApiDetailSpider,
):
    name = "universal_spider"

    def __init__(self, *args, **kwargs: dict[str, str]):
        super().__init__(name=self.name, **kwargs)
        packages = get_installed_packages()
        logger.info(f"installed packages: {packages}")

        self.default_playwright_meta = {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_context": self.name,
            "playwright_context_kwargs": {
                "ignore_https_errors": True,
                "viewport": {"width": 1920, "height": 1080},
                "locale": "zh-CN",
            },
            "playwright_page_goto_kwargs": {"wait_until": "networkidle"},
        }
        self.process_func = {
            "browser_list": self.browser_request_list,
            "browser_detail": self.browser_request_detail,
            "html_list": self.html_request_list,
            "html_detail": self.html_request_detail,
            "api_list": self.api_request_list,
            "api_detail": self.api_request_detail,
        }

    def start_requests(
        self,
    ) -> Generator[
        Callable[[str, list[dict[str, Any]], dict[str, Any], dict[str, Any]], Request],
        None,
        None,
    ]:
        logger.info(f"{self.name} start_requests")
        start_url = self.config["start_url"]
        stages = self.config["stages"]
        current_stage_index = 0
        current_stage = stages[current_stage_index]
        request_func = self.process_func.get(
            f"{current_stage['grab_method']}_{current_stage['type']}"
        )
        if request_func:
            yield request_func(
                start_url,
                stages,
                current_stage,
                **{"item": self.config["meta"]},
            )
