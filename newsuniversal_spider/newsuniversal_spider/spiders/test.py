import re

# 输入字符串
input_string = "6c620b64-2be2-4cce-a7fc-d97782221835,dba2bdfb-6361-46c1-a029-65c666103ac8,4604602a-bdc9-49c2-aca5-f9271eb9a909,6df90b55-b263-46b4-b228-9542c0e76c5e,aa627f8f-34e7-41c9-9331-5db559c0af7b"

# 正则表达式
uuid_pattern = r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"

# 替换所有 UUID 为 [UUID]
result = re.sub(uuid_pattern, '12323'+uuid_pattern, input_string)

# 输出结果
print("替换后的字符串:", result)