from typing import List, Any, Dict

from scrapy import Request
from newsuniversal_spider.spider_kit.request import Request as ApiRequest

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
                #"proxy": get_proxy(self.config, list_stage),
            },
            headers=headers,
            cookies=cookies,
            callback=self.html_parse_list,
            cb_kwargs=kwargs,
        )

    async def html_parse_list(
            self, response: HtmlResponse, **kwargs
    ) -> AsyncGenerator[Callable[[], Dict[str, Any] | Request], None]:
        meta = response.request.meta
        current_stage = meta["current_stage"]
        stages = meta["stages"]
        pre_item: Dict[str, Any] = kwargs.get("item") or {}
        default_max_page = 1
        default_current_page = 1
        max_page: int = current_stage.get("max_page") or default_max_page
        current_page: int = kwargs.get("current_page") or default_current_page

        org_items: Dict[str, Any] = await self.fields_loader(
            stage=current_stage,
            response=response,
            pre_item=pre_item,
            sort_results_by_xpath=True,
        )
        items = merge_items(org_items)

        logger.info(f"List Stage items: {items}")

        next_stage = self.get_next_stage(meta["stages"], current_stage)

        for item in items:
            item = await self.merge_files_fields(item, response)
            item = self.merge_subfields(item)
            item = merge_dict(pre_item, item)

            if next_stage:
                yield self.send_next_request(
                    next_stage, stages, item, item.get("api_url") or item.get("url")
                )
            else:
                yield self.generate_item(response.url, current_stage["type"], item)

        # 根据最大页数循环调用
        if current_page >= max_page:
            return

        next_page_url = await self.parse_next_page_link(response, current_stage)
        if next_page_url:
            request_func = self.process_func[
                f"{current_stage['grab_method']}_{current_stage['type']}"
            ]
            (
                next_page_params,
                next_page_form_data,
                next_page_json_data,
            ) = self.parse_next_page_api_payload(current_stage)
            yield request_func(
                next_page_url,
                stages,
                current_stage,
                **{
                    "current_page": current_page + 1,
                    "item": pre_item,
                    "params": next_page_params,
                    "form_data": next_page_form_data,
                    "json_data": next_page_json_data,
                },
            )


class ApiListSpider(BaseSpider):
    pass