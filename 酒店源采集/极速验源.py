import requests
from tqdm import tqdm
import threading
import time

def test_connectivity(url):
    try:
        response = requests.get(url, timeout=0.2)
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

with open("1.txt", "r", encoding='utf-8') as source_file, open("output.txt", "w", encoding='utf-8') as output_file:
    lines = source_file.readlines()
    for line in tqdm(lines, desc="Processing lines"):
        thread = threading.Thread(target=process_line, args=(line, output_file))
        thread.start()
        thread.join() # 去掉timeout参数，不再设置超时时间
        if thread.is_alive():
            #print(f"Skipping line due to timeout: {line}") # 注释掉这行代码，因为已经去掉了超时处理逻辑
            continue # 保留这行代码，确保在线程仍在运行时跳过当前行继续处理下一行数据
