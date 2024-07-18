import requests
from tqdm import tqdm
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import threading
from queue import Queue

#  获取远程港澳台直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/V4.txt"          #源采集地址
r = requests.get(url)
open('1.txt','wb').write(r.content)         #打开源文件并临时写入



def test_connectivity(url):
    try:
        response = requests.get(url, timeout=15)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_video_resolution(url):
    cap = cv2.VideoCapture(url)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height

def process_line(line, output_list):
    parts = line.strip().split(',')
    if len(parts) != 2:
        return
    channel_name, channel_url = parts
    if 'genre' in line.lower():
        output_list.append(line)
        return
    if test_connectivity(channel_url):
        width, height = get_video_resolution(channel_url)
        if height >= 720:
            output_list.append(f"{channel_name}[{width}x{height}],{channel_url}\n")####################{width}x{height}
    else:
        if '404' in str(test_connectivity(channel_url)):
            return

def worker(input_queue, output_list):
    while not input_queue.empty():
        line = input_queue.get()
        process_line(line, output_list)
        input_queue.task_done()

with open("1.txt", "r", encoding='utf-8') as source_file:
    lines = source_file.readlines()
    input_queue = Queue()
    for line in lines:
        input_queue.put(line)

    num_threads = 16
    threads = []
    output_list = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(input_queue, output_list))
        t.start()
        threads.append(t)

    input_queue.join()
    for t in threads:
        t.join()

    with open("有效源.txt", "w", encoding='utf-8') as output_file:
        for item in output_list:
            output_file.write(item)


os.remove("1.txt")
print("任务完成，输出有效源.txt")
