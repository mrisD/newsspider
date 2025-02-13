import json
from typing import Any, Iterable, List, Optional, Tuple, Union, cast
from urllib.parse import urlencode, urlsplit, urlunsplit

from loguru import logger
from scrapy import FormRequest
from scrapy.http.request.form import FormdataKVType
from scrapy.utils.python import is_listlike, to_bytes



FormdataType = JsondataType = Optional[
    Union[dict[str, Any], List[Tuple[str, str]], str]
]


def req_urlencode(seq: Iterable[FormdataKVType], enc: str) -> str:  #
    """
    重写 from scrapy.http.request.form import req_urlencode
    将v 强制转为 str 类型
    :param seq:
    :param enc:
    :return:
    """
    values = [
        (to_bytes(k, enc), to_bytes(str(v), enc))
        for k, vs in seq
        for v in (cast(Iterable[str], vs) if is_listlike(vs) else [cast(str, vs)])
    ]
    return urlencode(values, doseq=True)


class Request(FormRequest):
    """
    整合request formrequest jsonrequest方法
    """

    def __init__(
        self,
        *args,
        formdata: Optional[FormdataType] = None,  # type: ignore
        jsondata: Optional[JsondataType] = None,
        params: Optional[dict[str, Any] | str] = None,
        **kwargs,
    ) -> None:
        if kwargs.get("method") is None:
            if not jsondata and not formdata:
                kwargs["method"] = "GET"
            else:
                kwargs["method"] = "POST"
        else:
            kwargs["method"] = kwargs.get("method", "").upper()
        super().__init__(*args, **kwargs)
        if params:
            form_query_str = (
                req_urlencode(params.items(), self.encoding)
                if isinstance(params, dict)
                else params
            )
            self._set_url(urlunsplit(urlsplit(self.url)._replace(query=form_query_str)))
        if formdata and jsondata:
            logger.warning("formdata和jsondata同时传入 formdata将被无视 只使用jsondata")
        if not jsondata and formdata:
            if isinstance(formdata, dict):
                form_query_str = req_urlencode(formdata.items(), self.encoding)
            else:
                form_query_str = formdata
            self.headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            self._set_body(form_query_str)
        elif jsondata:
            items = jsondata
            form_query_str = items if isinstance(items, str) else json.dumps(items)
            self.headers.setdefault("Content-Type", "application/json")
            self.headers.setdefault(
                "Accept", "application/json, text/javascript, */*; q=0.01"
            )
            self._set_body(form_query_str)
        self.meta["fingerprint"] = (
            request_fingerprint(self)
            if not self.meta.get("fingerprint")
            else self.meta["fingerprint"]
        )
