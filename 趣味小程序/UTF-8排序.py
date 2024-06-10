
with open('1.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()

lines.sort()

with open('新.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)
