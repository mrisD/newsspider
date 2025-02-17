import re
from typing import Any

from jsonpath_ng.ext import parse as jsonpath_parse

# 定义一个常量，用于分隔相同类型内容不同路径的 jsonpath
SAME_KIND_SPLIT = "|"


class JsonParser:
    default_value = ""

    def _translate_jsonpath(self, json_path: str) -> str:
        """
        将输入的jsonpath 转换为符合jsonpath规范的格式
        :param json_path: 输入的jsonpath
        :return: 符合jsonpath规范的jsonpath格式
        """
        jsonpath_str = json_path
        jsonpath_str = (
            "$." + jsonpath_str if not jsonpath_str.startswith("$.") else jsonpath_str
        )
        # 去掉结尾存在的[]
        jsonpath_str = (
            jsonpath_str[:-2] if jsonpath_str.endswith("[]") else jsonpath_str
        )
        # re替换其中的[]
        jsonpath_str = re.sub(r"\[\]", "[*]", jsonpath_str)
        return jsonpath_str

    def parse(self, json_data: dict[str, Any] | list[Any], json_path: str):  # type: ignore
        """
        解析输入的jsonpath 获取内容
        data.ap[].title 假设ap是列表 使用[]即可获取列表中所有title的值
        data.ap[1].title 在[]加入数字=python中list[1]获取索引为1的title值
        data.ap.title 如果ap不是列表则不加[] 直接获取该路径下的title值
        data.ap.title|data.ddddd.title 使用`|`连接可以同时获取多种路径下的值
        :param json_data: json类型数据
        :param jsonpath: json路径
        :return: 解析结果
        """
        value_list = []
        json_path_list = json_path.split(SAME_KIND_SPLIT)
        for path in json_path_list:
            if path.strip() == "*":
                value_list.append(json_data)
            else:
                parser = jsonpath_parse(self._translate_jsonpath(path))
                value_list_part = [i.value for i in parser.find(json_data)]
                if value_list_part:
                    value_list.extend(value_list_part)

        if len(value_list) == 1:
            value_list = value_list[0]
        elif len(value_list) == 0:
            value_list = self.default_value
        return value_list
