import requests
from tqdm import tqdm
import threading
import time
import os


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

def process_line(line, output_file):
    parts = line.strip().split(',')
    if len(parts) != 2:
        return
    channel_name, channel_url = parts
    if 'genre' in line.lower():
        output_file.write(line)
        return
    if test_connectivity(channel_url):
        output_file.write(f"{channel_name},{channel_url}
")
    else:
        return

with open("1.txt", "r", encoding='utf-8') as source_file, open("有效源.txt", "w", encoding='utf-8') as output_file:
    lines = source_file.readlines()
    for line in tqdm(lines, desc="Processing lines"):
        thread = threading.Thread(target=process_line, args=(line, output_file))
        thread.start()
        thread.join(timeout=2) # 设置线程超时时间，如果线程在指定时间内未完成，将被强制终止。这样可以避免某些行由于网络问题导致处理时间过长而影响整体进度。同时，这也确保了主进程可以在所有行都被处理后安全地退出。但注意这并不能解决所有的网络问题，只能在一定程度上减少因网络问题导致的处理延迟。此外，如果某些行的连接检查失败，它们会被跳过并继续处理下一行，而不是被阻塞等待连接恢复。这样可以提高程序的健壮性和效率。


os.remove("1.txt")
print("任务运行完毕")
