import requests
from tqdm import tqdm
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


#  获取远程港澳台直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/V4.txt"          #源采集地址
r = requests.get(url)
open('1.txt','wb').write(r.content)         #打开源文件并临时写入


def test_connectivity(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_line(line, output_file):
    parts = line.strip().split(',')
    if len(parts) != 2:
        return
    channel_name, channel_url = parts
    if 'genre' in line.lower():
        output_file.write(line)
        return
    if test_connectivity(channel_url):
        output_file.write(f"{channel_name},{channel_url}\n")
    else:
        return

with open("1.txt", "r", encoding='utf-8') as source_file, open("有效源.txt", "w", encoding='utf-8') as output_file:
    lines = source_file.readlines()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_line, line, output_file): line for line in lines}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing lines"):
            try:
                future.result()
            except Exception as e:
                print(f"Skipping line due to error: {futures[future]}")

os.remove("1.txt")
print("任务完成，输出有效源.txt")
