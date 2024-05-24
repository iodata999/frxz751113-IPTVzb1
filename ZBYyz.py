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
import eventlet

with open("iptvsearch/1.txt", 'r', encoding='utf-8') as file:


 eventlet.monkey_patch()

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
# 从iptv.txt文件内提取其他频道进行检测并分组
with open("iptvsearch/1.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            channel_name, channel_url = line.split(',')
            if 'genre' not in channel_url:
                channels.append((channel_name, channel_url))


# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(0.8, False):  #################////////////////////////////////
                start_time = time.time()
                content = requests.get(ts_url).content
                end_time = time.time()
                response_time = (end_time - start_time) * 0.5

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                # print(f"文件大小：{file_size} 字节")
                download_speed = file_size / response_time / 1024
                # print(f"下载速度：{download_speed:.3f} kB/s")
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                # print(f"标准化后的速率：{normalized_speed:.3f} MB/s")

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(
                    f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(
                f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 16
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    # t = threading.Thread(target=worker, args=(event,len(channels)))  # 将工作线程设置为守护线程
    t.start()
    # event.set()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()


def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字


# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))
result_counter = 10  # 每个频道需要的个数

with open("hn.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name or 'CCTV3' in channel_name or 'CCTV6' in channel_name or 'CCTV8' in channel_name or 'CCTV13' in channel_name or 'CCTV15' in channel_name or '4K' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '湖北卫视' in channel_name or '凤凰卫视' in channel_name or '湖南卫视' in channel_name or '石家庄娱乐' in channel_name or '江苏卫视' in channel_name or '山东卫视' in channel_name or '安徽卫视' in channel_name or '北京卫视' in channel_name or '广东卫视' in channel_name or '广东珠江' in channel_name or '贵州卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('地方频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        #if '龙祥' in channel_name or '酒店' in channel_name or 'AXN' in channel_name or '东森' in channel_name or '澳门莲花' in channel_name or '天映' in channel_name or '星空' in channel_name or '星河' in channel_name or '私人' in channel_name or '凤凰' in channel_name:
        if 'CCTV' not in channel_name and '卫视' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1


    channel_counters = {}
    file.write('港澳频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '龙祥' in channel_name or '酒店' in channel_name or 'AXN' in channel_name or '东森' in channel_name or '澳门莲花' in channel_name or '天映' in channel_name or '好莱坞' in channel_name or 'TVB星河' in channel_name or '私人' in channel_name or '凤凰' in channel_name or '星空' in channel_name:
          #if 'CCTV' not in channel_name and '卫视' not in channel_name and 'TV' not in channel_name and '儿' not in channel_name and '文' not in channel_name and 'CHC' not in channel_name and '新' not in channel_name and '山东' not in channel_name and '河北' not in channel_name and '哈哈' not in channel_name and '临沂' not in channel_name and '公共' not in channel_name and 'CETV' not in channel_name and '交通' not in channel_name and '冬' not in channel_name and '梨园' not in channel_name and '民生' not in channel_name and '综合' not in channel_name and '法制' not in channel_name and '齐鲁' not in channel_name and '自办' not in channel_name and '都市' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
      
# 合并自定义频道文件内容
file_contents = []
file_paths = ["hn.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("#自用.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("hn.txt")
print("任务运行完毕，分类频道列表可查看文件夹内.txt文件！")
