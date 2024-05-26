import time
import os
import re
import base64
import datetime
import requests
import threading
from queue import Queue
from datetime import datetime


input_file=结果.txt
output_file=结果.m3u

    # 读取txt文件内容
for line in fileinput.input("结果.txt", inplace=True): 
        lines = f.readlines()

    # 打开m3u文件并写入内容
with open(结果.m3u, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')

        # 初始化genre变量
        genre = ''

        # 遍历txt文件内容
        for line in lines:
            line = line.strip()
            if "," in line:  # 防止文件里面缺失“,”号报错
                # if line:
                # 检查是否是genre行
                channel_name, channel_url = line.split(',', 1)
                if channel_url == '#genre#':
                    genre = channel_name
                    print(genre)
                else:
                    # 将频道信息写入m3u文件
                    ##EXTINF:-1 tvg-id="" tvg-name="" tvg-logo="https://raw.githubusercontent.com/linitfor/epg/main/logo/壹電視新聞.png" group-title="直播新聞",壹電視新聞
                    ##EXTINF:-1 group-title="台灣",民視
                    f.write(f'#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/linitfor/epg/main/logo/{channel_name}.png" group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')


# 将txt文件转换为m3u文件
print(f"成功寫出M3U file")
