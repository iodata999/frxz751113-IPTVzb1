
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

with open("example.txt", "r") as file:
    sorted_content = sorted(file, key=lambda line: line.strip())
    for line in sorted_content:
        print(line)
result_counter = 10  # 每个频道需要的个数








with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")
