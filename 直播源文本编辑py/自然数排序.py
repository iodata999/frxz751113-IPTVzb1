import re
import pypinyin

def sort_lines(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 分离数字和非数字行
    number_lines = []
    non_number_lines = []
    for line in lines:
        if re.match(r'^\d+$', line.strip()):
            number_lines.append(line)
        else:
            non_number_lines.append(line)

    # 对数字行按大小排序
    number_lines.sort(key=lambda x: int(x.strip()))

    # 对非数字行按拼音顺序排序
    non_number_lines.sort(key=lambda x: pypinyin.lazy_pinyin(x.strip())[0][0])

    # 合并排序后的行
    sorted_lines = number_lines + non_number_lines

    # 将排序后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(sorted_lines)

# 使用示例：
file_path = "四川电信.txt"  # 替换为你的文件路径
sort_lines(file_path)
