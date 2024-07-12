import re
from pypinyin import lazy_pinyin

# 打开一个utf-8编码的文本文件
with open("input.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))

# 将排序后的行写入新的utf-8编码的文本文件
with open("output.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)
