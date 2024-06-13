#!/usr/bin/python3
import re
import subprocess

def get_resolution_from_file(file_path):
    try:
        results = []  # 用于存储检测结果

        with open(file_path, 'r', encoding='utf-8') as file:
            # 从txt文件中读取内容
            m3u8_content = file.read()

            # 使用正则表达式提取M3U8文件中的链接和频道名称
            video_channels = re.findall(r'([^,]+),\s*(https?://[^\s]+)', m3u8_content)

            for channel_name, video_url in video_channels:
                print(f"获取到频道名称: {channel_name}")
                print(f"获取到视频链接: {video_url}")

                try:
                    # 使用FFprobe获取分辨率信息（需要安装FFprobe）
                    resolution_output = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_url])
                    resolution = resolution_output.decode('utf-8').strip()
                    print(f"视频分辨率: {resolution}")

                    # 将结果添加到列表中
                    result_str = f"频道名称: {channel_name}\n视频链接: {video_url}\n视频分辨率: {resolution}\n" + "=" * 30
                    results.append(result_str)
                except subprocess.CalledProcessError as e:
                    print(f"无法获取分辨率信息：{str(e)}")
                    result_str = f"频道名称: {channel_name}\n视频链接: {video_url}\n无法获取分辨率信息\n" + "=" * 30
                    results.append(result_str)

        # 将结果写入txt文件
        with open('check_tv', 'w', encoding='utf-8') as result_file:
            for result in results:
                result_file.write(result + "\n\n")
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到")

# 替换为你的M3U8文件路径
m3u8_file_path = 'IPTV.txt'
get_resolution_from_file(m3u8_file_path)
