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

import eventlet



with open("合并.txt", 'w', encoding='utf-8') as file:
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


 
# 合并自定义频道文件内容
file_contents = []
file_paths = ["合并.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("iptv_list.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")
print("任务运行完毕，分类频道列表可查看文件夹内iptv_list.txt文件！")
