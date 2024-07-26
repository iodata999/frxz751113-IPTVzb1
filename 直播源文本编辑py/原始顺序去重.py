# 打开文档并读取所有行 
with open('1.txt', 'r', encoding="utf-8") as file:
    lines = file.readlines()

# 使用列表来存储唯一的行的顺序 
unique_lines = [] 
seen_lines = set() 

# 打印去重前的行数
print(f"去重前的行数: {len(lines)}")

# 遍历每一行，如果是新的就加入unique_lines 
for line in lines:
    line_stripped = line.strip()  # 去除行尾的换行符
    if line_stripped not in seen_lines:
        unique_lines.append(line)  # 保持原始行的格式，包括换行符
        seen_lines.add(line_stripped)

# 将唯一的行写入新的文档 
with open('q.txt', 'w', encoding="utf-8") as file:
    file.writelines(unique_lines)

# 打印去重后的行数
print(f"去重后的行数: {len(unique_lines)}")
