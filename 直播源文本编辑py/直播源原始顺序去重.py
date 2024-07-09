a = input('FileName(DragHere):')

with open(a, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    before = len(lines)
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    after = len(unique_lines)
with open(a, 'w', encoding="utf-8") as f:
    f.writelines(unique_lines)

print('处理完成：')
print(f'处理前文件行数：{before}')
print(f'处理后文件行数：{after}')
input()
