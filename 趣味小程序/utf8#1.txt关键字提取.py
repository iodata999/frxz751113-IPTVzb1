import re
with open('1.txt', 'r') as f:
    
 keywords = [',', 'genre']  # 需要提取的关键字列表
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
 with open('1.txt', 'r', encoding='UTF-8') as file, open('新x.txt', 'w', encoding='utf-8') as TW:
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         TW.write(line)  # 将该行写入输出文件
            

print("任务运行完毕，分类频道列表可查看文件夹内新.txt文件！")
