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

# 合并自定义频道文件内容
file_contents = []
file_paths = ["广东电信.txt", "四川电信.txt", "安徽电信.txt", "湖北电信.txt", "北京联通.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("合并.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))


print("任务运行完毕，分类频道列表可查看文件夹内合并.txt文件！")
