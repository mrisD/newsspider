from typing import List, Any, Dict

from scrapy import Request

from newsuniversal_spider.newsuniversal_spider.spiders.base import BaseSpider


class HtmlListSpider(BaseSpider):
    def html_request_list(
            self,
            url: str,
            stages: List[Dict[str, Any]],
            list_stage: Dict[str, Any],
            **kwargs,  # type: ignore
    ) -> Request:
        params = kwargs.get("params") or list_stage.get("params")
        form_data = kwargs.get("form_data") or list_stage.get("form_data")
        json_data = kwargs.get("json_data") or list_stage.get("json_data")
        headers = kwargs.get("headers") or list_stage.get("headers")
        cookies = kwargs.get("cookies") or list_stage.get("cookies")
        return ApiRequest(
            url=self.replace_api_payload(url),
            params=self.replace_api_payload(params),
            formdata=self.replace_api_payload(form_data),
            jsondata=self.replace_api_payload(json_data),
            method=list_stage.get("method") or "GET",
            dont_filter=True,
            meta={
                "stages": stages,
                "current_stage": list_stage,
                "proxy": get_proxy(self.config, list_stage),
            },
            headers=headers,
            cookies=cookies,
            callback=self.html_parse_list,
            cb_kwargs=kwargs,
        )


class ApiListSpider(BaseSpider):
    pass