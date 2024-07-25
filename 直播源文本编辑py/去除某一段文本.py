# 定义关键词
start_keyword = '港澳频道,#genre#'
end_keyword = '湖北湖南,#genre#'

# 输入输出文件路径
input_file_path = '分类.txt'  # 替换为你的输入文件路径
output_file_path = '22.txt'  # 替换为你想要保存输出的文件路径

# 标记是否处于要删除的行范围内
delete_range = False

# 读取原始文件并过滤掉指定范围内的行
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 过滤掉不需要的行
filtered_lines = []
for line in lines:
    # 如果找到开始关键词，标记开始删除范围，并跳过这一行
    if start_keyword in line:
        delete_range = True
        continue
    # 如果找到结束关键词，标记结束删除范围，添加这一行并重置删除标记
    elif end_keyword in line:
        delete_range = False
    # 如果当前不在删除范围内，保留这行
    if not delete_range:
        filtered_lines.append(line)

# 将过滤后的内容写入新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print('过滤完成，结果已保存到:', output_file_path)
