import requests
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
from queue import Queue
from datetime import datetime
import replace
import fileinput

#  获取远程港澳台直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/TW.txt"          #源采集地址
r = requests.get(url)
open('1.txt','wb').write(r.content)         #打开源文件并临时写入




def test_connectivity(url):
    try:
        response = requests.get(url, timeout=1)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_line(line, output_file, order_list):
    parts = line.strip().split(',')
    if len(parts) != 2:
        return
    channel_name, channel_url = parts
    if 'genre' in line.lower():
        output_file.write(line)
        return
    if test_connectivity(channel_url):
        output_file.write(f"{channel_name},{channel_url}\n")
        order_list.append((channel_name, channel_url))
    else:
        return

valid_count = 0
invalid_count = 0
order_list = []

with open("1.txt", "r", encoding='utf-8') as source_file, open("有效源.txt", "w", encoding='utf-8') as output_file:
    lines = source_file.readlines()
    with ThreadPoolExecutor(max_workers=16) as executor:###此行调整线程
        futures = {executor.submit(process_line, line, output_file, order_list): line for line in lines}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing lines"):
            result = future.result()
            if result is not None:
                valid_count += 1
            else:
                invalid_count += 1
#os.remove("1.txt")
print("任务完成，输出有效源.txt")
