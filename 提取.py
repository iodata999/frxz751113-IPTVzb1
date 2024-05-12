import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
from datetime import datetime

open('广东电信.txt','wb').write(re.content)         #打开源文件名

keywords = ['重温经典', 'CCTV','热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('广东电信.txt', 'r', encoding='utf-8') as file, open('TW.txt', 'w', encoding='utf-8') as TW:
    TW.write('\n数字频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          TW.write(line)  # 将该行写入输出文件

# 读取要合并的香港频道和台湾频道文件
file_contents = []
file_paths = ["TW.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))



      
# 合并自定义频道文件内容
file_contents = []
file_paths = ["GAT.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("iptv_list.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("iptv.txt")
os.remove("GAT.txt")
os.remove("hn.txt")
#os.remove("HK.txt")
os.remove("DIYP-v4.txt")
os.remove("TW.txt")
print("任务运行完毕，分类频道列表可查看文件夹内iptv_list.txt文件！")
