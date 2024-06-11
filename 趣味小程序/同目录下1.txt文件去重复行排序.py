
with open("1.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
    before = len(lines)
    lines = list(set(lines))
    after = len(lines)

lines.sort()

with open('1.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)
print('处理完成：')
print(f'处理前文件行数：{before}')
print(f'处理后文件行数：{after}')
input()
