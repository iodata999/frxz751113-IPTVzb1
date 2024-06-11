import replace
import fileinput
import re
import os
with open("酒店源.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
    before = len(lines)
    lines = list(set(lines))
    after = len(lines)

lines.sort()

with open('2.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)
print('处理完成：')
print(f'处理前文件行数：{before}')
print(f'处理后文件行数：{after}')






###############################        
with open('2.txt', 'r', encoding='utf-8') as file:
#从整理好的文本中按类别进行特定关键词提取#############################################################################################
 keywords = ['CCTV', '风云', '兵器', '女性', '地理', '央视文化', '风云', '怀旧剧场', '第一剧场', 'CHC']  # 需要提取的关键字列表
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:    #####定义临时文件名
    a.write('\n央视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         a.write(line)  # 将该行写入输出文件 

################
keywords = ['卫视']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:    #####定义临时文件名
    b.write('\n卫视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         b.write(line)  # 将该行写入输出文件

         
################
keywords = ['影', '剧', '妈', '功夫', '惊']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n影视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件

############
keywords = ['http']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
with open('2.txt', 'r', encoding='utf-8') as file, open('d.txt', 'w', encoding='utf-8') as d:    #####定义临时文件名
    d.write('\n其他频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if 'CCTV' not in line and '卫视' not in line:
          if re.search(pattern, line): 
              d.write(line)  # 将该行写入输出文件

############
file_contents = []
file_paths = ["a.txt", "b.txt", "c.txt", "d.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("新.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

os.remove("a.txt")
os.remove("b.txt")
os.remove("c.txt")
os.remove("d.txt")
os.remove("2.txt")
print("任务运行完毕")






