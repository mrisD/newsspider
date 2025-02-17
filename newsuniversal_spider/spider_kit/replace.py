import re

# 匹配类型和类型值的正则表达式
TYPE_PATTERN = r"\{(?P<type>[a-zA-Z_]+)\:"

# 匹配分页函数名和函数参数
PAGE_FUNCTION_PATTERN = r"\{(?P<type>page_function)\:(?P<function_name>\w+)\((?P<function_params>[^\}]*)\)\}"  # noqa E501

# jsonpath的正则表达式
JSONPATH_PATTERN = r"\{(?P<type>jsonpath)\:(?P<jsonpath>[^\}]*)\}"

# 匹配函数名和函数参数的正则表达式
FUNCTION_PATTERN = (
    r"\{(?P<type>function)\:(?P<function_name>\w+)\((?P<function_params>[^\}]*)\)\}"
)

# xpath的正则表达式
XPATH_PATTERN = r"\{(?P<type>xpath)\:(?P<xpath>[^\}]*)\}"

# re的正则表达式
RE_PATTERN = r"\{(?P<type>re)(?P<flag>A|I|L|U|M|S|X|T)?\:(?P<re>[^\}]*)\}"

types_pattern = {
    "jsonpath": JSONPATH_PATTERN,
    "page_function": PAGE_FUNCTION_PATTERN,
    "function": FUNCTION_PATTERN,
    "xpath": XPATH_PATTERN,
    "re": RE_PATTERN,
}

class Replacer():
    def __init__(self):
        pass
    def replace_page_function(self, text,current_page):
        # 正则表达式匹配 {page_function:page_number(arg1,arg2,arg3)}
        pattern = r"\{page_function:page_number\((\d+),?(\d*),?(\d*)\)\}"

        # 用于替换的函数
        def replacement(match):
            # 提取初始值arg1，步长arg2，最大值arg3
            arg1 = int(match.group(1))
            arg2 = match.group(2)
            if arg2 !='':
                arg2 = int(arg2)
            else:
                arg2=1
            arg3 = match.group(3)

            # 如果 arg3 是空的，就设置为无上限
            if arg3:
                arg3 = int(arg3)
            else:
                arg3 = float('inf')  # 设置为无穷大，表示不限制

            # 计算新页码
            page_number = arg1 + (current_page - 1) * arg2

            # 如果最大值 arg3 被提供，确保页码不超过最大值
            if page_number > arg3:
                page_number = arg3

            return str(page_number)

        # 使用正则替换匹配到的内容
        result = re.sub(pattern, replacement, text)

        return result
    def replace(self,text,current_page):
        typelist=re.findall(TYPE_PATTERN, text)
        if "page_function" in typelist:
            text=self.replace_page_function(text,current_page)
        return text

if __name__ == "__main__":
    text="https://www.ycs.gov.cn/ywdt/yczx_{page_function:page_number(1)}"
    rep=Replacer()
    print(rep.replace(text,5))

