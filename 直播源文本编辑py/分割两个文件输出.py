# 定义关键词
start_keyword = '港澳频道,#genre#'
end_keyword = '湖北湖南,#genre#'

# 输入输出文件路径
input_file_path = '分类.txt'  # 替换为你的输入文件路径
output_file_path = '22.txt'  # 替换为你想要保存输出的文件路径
deleted_lines_file_path = 'cc.txt'  # 替换为你想要保存删除行的文件路径


# 标记是否处于要删除的行范围内
delete_range = False
# 存储要删除的行，包括开始关键词行
deleted_lines = []

# 读取原始文件并过滤掉指定范围内的行
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 过滤掉不需要的行
filtered_lines = []
for line in lines:
    if start_keyword in line:
        delete_range = True
        deleted_lines.append(line)  # 将开始关键词行添加到删除行列表
        continue
    if delete_range:
        if end_keyword in line:
            delete_range = False
            filtered_lines.append(line)  # 将结束关键词行添加到输出文件列表
        else:
            deleted_lines.append(line)  # 添加到删除行列表
    else:
        filtered_lines.append(line)

# 将过滤后的内容写入新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

# 将删除的行写入到新的文件中
with open(deleted_lines_file_path, 'w', encoding='utf-8') as file:
    file.writelines(deleted_lines)

print('过滤完成，结果已保存到:', output_file_path)
print('删除的行已保存到:', deleted_lines_file_path)
