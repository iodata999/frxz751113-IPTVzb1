
from opencc import OpenCC

# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
#converter = OpenCC('t2s.json')#繁转简
converter = OpenCC('s2t.json')#简转繁
# 打开itv.txt文件
with open('结果.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入itv.txt文件
with open('i结果.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)
