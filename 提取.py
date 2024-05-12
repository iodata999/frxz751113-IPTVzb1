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


url = "https://raw.githubusercontent.com/frxz751113/IPTVzb1/main/合并.txt"          #源采集地址
r = requests.get(url)
open('合并.txt','wb').write(r.content)         #打开源文件名
                            # 替换特定文字
if name in text:
  name = name.replace("中央", "CCTV")  
  name = name.replace("高清", "")  
  name = name.replace("HD", "")  
  name = name.replace("标清", "")  
  name = name.replace("超高", "")  
  name = name.replace("频道", "")  
  name = name.replace("-", "")  
  name = name.replace(" ", "")  
  name = name.replace("PLUS", "+")  
  name = name.replace("＋", "+")  
  name = name.replace("cctv", "CCTV")
  name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)  
  name = name.replace("CCTV1综合", "CCTV1")  
  name = name.replace("CCTV2财经", "CCTV2")  
  name = name.replace("CCTV3综艺", "CCTV3")  
  name = name.replace("CCTV4国际", "CCTV4")  
  name = name.replace("CCTV4中文国际", "CCTV4")  
  name = name.replace("CCTV4欧洲", "CCTV4")  
  name = name.replace("CCTV5体育", "CCTV5")  
  name = name.replace("CCTV5+体育", "CCTV5+")  
  name = name.replace("CCTV6电影", "CCTV6")  
  name = name.replace("CCTV7军事", "CCTV7")  
  name = name.replace("CCTV7军农", "CCTV7")  
  name = name.replace("CCTV7农业", "CCTV7")  
  name = name.replace("CCTV7国防军事", "CCTV7")  
  name = name.replace("CCTV8电视剧", "CCTV8")  
  name = name.replace("CCTV8纪录", "CCTV9")  
  name = name.replace("CCTV9记录", "CCTV9")  
  name = name.replace("CCTV9纪录", "CCTV9")  
  name = name.replace("CCTV10科教", "CCTV10")  
  name = name.replace("CCTV11戏曲", "CCTV11")  
  name = name.replace("CCTV12社会与法", "CCTV12")  
  name = name.replace("CCTV13新闻", "CCTV13")  
  name = name.replace("CCTV新闻", "CCTV13")  
  name = name.replace("CCTV14少儿", "CCTV14")  
  name = name.replace("央视14少儿", "CCTV14")  
  name = name.replace("CCTV少儿超", "CCTV14")  
  name = name.replace("CCTV15音乐", "CCTV15")  
  name = name.replace("CCTV音乐", "CCTV15")  
  name = name.replace("CCTV16奥林匹克", "CCTV16")  
  name = name.replace("CCTV17农业农村", "CCTV17")  
  name = name.replace("CCTV17军农", "CCTV17")  
  name = name.replace("CCTV17农业", "CCTV17")  
  name = name.replace("测试）", "")  


results.append(f"{name},{urld}")


channels = []

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


url = "https://raw.githubusercontent.com/frxz751113/IPTVzb1/main/合并.txt"          #源采集地址
r = requests.get(url)
open('合并.txt','wb').write(r.content)         #打开源文件名# 替换特定文字

keywords = ['重温经典', 'CCTV','热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('TW.txt', 'w', encoding='utf-8') as TW:
    TW.write('\n央视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          TW.write(line)  # 将该行写入输出文件
            

keywords = ['重温经典', '卫视','热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('ws.txt', 'w', encoding='utf-8') as ws:
    ws.write('\n卫视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          ws.write(line)  # 将该行写入输出文件

keywords = ['重温经典', '影', '剧', '娱乐', '热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('df.txt', 'w', encoding='utf-8') as df:
    df.write('\n地方频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          df.write(line)  # 将该行写入输出文件

# 读取要合并的香港频道和台湾频道文件
file_contents = []
file_paths = ["TW.txt", "ws.txt", "df.txt"]  # 替换为实际的文件路径列表
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
with open("结果.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("合并.txt")
os.remove("GAT.txt")
os.remove("ws.txt")
os.remove("df.txt")
#os.remove("DIYP-v4.txt")
os.remove("TW.txt")
print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")

keywords = ['重温经典', 'CCTV','热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('TW.txt', 'w', encoding='utf-8') as TW:
    TW.write('\n央视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          TW.write(line)  # 将该行写入输出文件
            

keywords = ['重温经典', '卫视','热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('ws.txt', 'w', encoding='utf-8') as ws:
    ws.write('\n卫视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          ws.write(line)  # 将该行写入输出文件

keywords = ['重温经典', '影', '剧', '娱乐', '热剧 8M1080', '超级电影 8M1080', '超级电视剧 8M1080', '喜剧 8M1080', '惊悚悬疑 8M1080', '明星大片 8M1080', '潮妈辣婆 8M1080', '精品大剧 8M1080', '动作电影 8M1080', '古装剧场 8M1080', '中国功夫 8M1080', '神乐剧场']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('合并.txt', 'r', encoding='utf-8') as file, open('df.txt', 'w', encoding='utf-8') as df:
    df.write('\n地方频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          df.write(line)  # 将该行写入输出文件

# 读取要合并的香港频道和台湾频道文件
file_contents = []
file_paths = ["TW.txt", "ws.txt", "df.txt"]  # 替换为实际的文件路径列表
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
with open("结果.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("合并.txt")
os.remove("GAT.txt")
os.remove("ws.txt")
os.remove("df.txt")
#os.remove("DIYP-v4.txt")
os.remove("TW.txt")
print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")
