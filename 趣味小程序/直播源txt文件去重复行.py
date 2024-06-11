a = input('FileName(DragHere):')

with open(a, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    before = len(lines)
    lines = list(set(lines))
    after = len(lines)
with open(a, 'w', encoding="utf-8") as f:
    f.writelines(lines)

print('处理完成：')
print(f'处理前文件行数：{before}')
print(f'处理后文件行数：{after}')
input()
