import re
import requests
import concurrent.futures

# 定义一个函数，用于测试频道的连通性
def test_connectivity(channel_name, channel_url):
    try:
        # 发送GET请求，设置超时时间为2秒
        response = requests.get(channel_url, timeout=2)
        if response.status_code == 200:
            # 如果响应状态码为200，返回频道名称、频道URL和成功信息
            return channel_name, channel_url, "Success"
        else:
            # 如果响应状态码不为200，返回频道名称、频道URL和失败信息
            return channel_name, channel_url, "Failed"
    except:
        # 如果发生异常，返回频道名称、频道URL和失败信息
        return channel_name, channel_url, "Failed"

# 定义一个函数，用于提取频道名称中的数字作为关键字
def channel_key(channel):
    match = re.search(r'\d+', channel)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 如果没有找到数字，返回一个无穷大的数字作为关键字

# 读取IPTV.txt文件中的频道信息，并将其添加到channels列表中
channels = []
with open("酒店源.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            if 'rtp' in line or 'udp' in line:
                pass
            else:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))

# 使用线程池并发地测试频道的连通性
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for channel in channels:
        channel_name, channel_url = channel
        futures.append(executor.submit(test_connectivity, channel_name, channel_url))

    # 收集所有线程的结果
    results = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        results.append(result)

# 将结果按照频道名称排序
results.sort(key=lambda x: x[0])

# 将排序后的结果写入connectivity_results.txt文件
with open("IPTV_list.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, status = result
        file.write(f"{channel_name},{channel_url},{status}")

# 从connectivity_results.txt文件中读取有效的频道信息（即状态不为"Failed"）
channels = []
with open("IPTV_list.txt", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            channel_name, channel_url, status = line.split(',')
            if status != "Failed":
                channels.append((channel_name,channel_url))

# 对频道进行排序，关键字为频道名称中的数字
channels.sort(key=lambda x: channel_key(x[0]))

# 将排序后的频道信息写入IPTV_connectivity.txt文件
with open("IPTV_list.txt", 'w', encoding='utf-8') as file:
    for channel_name,channel_url in channels:
        file.write(f'{channel_name},{channel_url}')
