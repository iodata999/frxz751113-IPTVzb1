# 定义关键词
start_keyword = '港澳频道,#genre#'
end_keyword = '湖北湖南,#genre#'

# 输入输出文件路径
input_file_path = '分类.txt'  # 替换为你的输入文件路径
output_file_path = '22.txt'  # 替换为你想要保存输出的文件路径

# 用于存储结果的列表
result_lines = []

# 打开输入文件并读取内容
with open(input_file_path, 'r', encoding='utf-8') as file:
    capture = False  # 用于控制是否开始捕获行
    for line in file:
        # 检查是否到达开始关键词
        if start_keyword in line:
            capture = True
        # 如果已经开始捕获，并且到达结束关键词，则停止捕获
        elif end_keyword in line and capture:
            break
        # 如果处于捕获状态，则添加当前行
        if capture:
            result_lines.append(line)

# 将结果写入输出文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(result_lines)

print('提取完成，结果已保存到:', output_file_path)
