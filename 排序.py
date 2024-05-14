
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
import replace
import fileinput

url = "https://raw.githubusercontent.com/frxz751113/IPTVzb1/main/合并.txt"          #源采集地址
r = requests.get(url)
open('合并.txt','wb').write(r.content)         #打开源文件
# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))
result_counter = 10  # 每个频道需要的个数








with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")
