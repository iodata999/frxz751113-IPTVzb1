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
import time
import json
import concurrent.futures

hebei = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki"        #河北
shaanxi = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D"    #陕西
liaoning = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ibGlhb25pbmci"    #辽宁
fujian = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D"    #福建
henan = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D"    #河南
hubei = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5YyXIg%3D%3D"    #湖北

def process_url(url):
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    #urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls: # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    urls = set(x_urls) # 去重得到唯一的URL列表

    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers = 100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)

    for url in valid_urls:
        print(url)
    # 遍历网址列表，获取JSON文件并解析
    results = []
    for url in valid_urls:
        try:
            # 发送GET请求获取JSON文件，设置超时时间为0.5秒
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]  # http:// or https://
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"
            
            json_url = f"{url}"
            response = requests.get(json_url, timeout=0.5)
            json_data = response.json()

            try:
                # 解析JSON文件，获取name和url字段
                for item in json_data['data']:
                    if isinstance(item, dict):
                        name = item.get('name')
                        urlx = item.get('url')
                        if 'http' in urlx.lower():
                            urld = f"{urlx}"
                        else:
                            urld = f"{url_x}{urlx}"
                        results.append((name, urld))
            except KeyError:
                pass
        except ValueError:
            continue

    return results

# 调用函数并打印结果
url = "http://example.com"  # 替换为你要访问的网页地址
result = process_url(url)
for name, url in result:
    print(f"{name}: {url}")

                        if name and urlx:
                            # 删除特定文字
                            name = name.replace("中央", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("频道", "")
                            name = name.replace("-", "")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace(")", "")
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            if 'udp' in urld or 'rtp' in urld:
                                pass
                            else:
                                results.append(f"{name},{urld}")
            except:
                continue
        except:
            continue

    return results
def save_results(results, filename):
    # 将结果保存到文本文件
    with open(filename, "w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")
            print(result)

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass

    return None

# 处理第1个URL
results_hebei = process_url(hebei)
save_results(results_hebei, "hebei.txt")



# 处理第8个URL
results_shaanxi = process_url(shaanxi)
save_results(results_shaanxi, "shaanxi.txt")

# 处理第9个URL
results_liaoning = process_url(liaoning)
save_results(results_liaoning, "liaoning.txt")


# 处理第13个URL
results_fujian = process_url(fujian)
save_results(results_fujian, "fujian.txt")


# 处理第16个URL
results_henan = process_url(henan)
save_results(results_henan, "henan.txt")

# 处理第17个URL
results_hubei = process_url(hubei)
save_results(results_hubei, "hubei.txt")

# 合并文件内容
file_contents = []
file_paths = ["hebei.txt",  "shaanxi.txt", "liaoning.txt",  "fujian.txt", "henan.txt", "hubei.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("IPTV.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
# 定义一个函数，用于测试频道的响应速度
def test_speed(channel_name, channel_url):
    try:
        # 发送GET请求，设置超时时间为2秒
        response = requests.get(channel_url, timeout=2)
        if response.status_code == 200:
            # 如果响应状态码为200，计算响应时间并返回频道名称、频道URL和响应时间
            speed = response.elapsed.total_seconds()
            return channel_name, channel_url, f"{speed:.3f} seconds"
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
with open("IPTV.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            if 'rtp' in line or 'udp' in line:
                pass
            else:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))

# 使用线程池并发地测试频道的响应速度
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for channel in channels:
        channel_name, channel_url = channel
        futures.append(executor.submit(test_speed, channel_name, channel_url))

    # 收集所有线程的结果
    results = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        results.append(result)

# 将结果按照频道名称和响应时间排序
results.sort(key=lambda x: (x[0], x[2]))

# 将排序后的结果写入IPTV_list文件
with open("IPTV1_list", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}")

# 从IPTV_list文件中读取有效的频道信息（即响应时间不为"Failed"）
channels = []
with open("IPTV1_list", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            channel_name, channel_url, speed = line.split(',')
            if speed != "Failed":
                channels.append((channel_name,channel_url))

# 对频道进行排序，关键字为频道名称中的数字
channels.sort(key=lambda x: channel_key(x[0]))

# 将排序后的频道信息写入IPTV_speed.txt文件
with open("酒店源.txt", 'w', encoding='utf-8') as file:
    for channel_name,channel_url in channels:
        file.write(f'{channel_name},{channel_url}')


#任务结束，删除不必要的过程文件###########################################################################################################################
files_to_remove = ["hebei.txt",  "shaanxi.txt", \
                   "liaoning.txt",  "fujian.txt",  "henan.txt", "hubei.txt", \
                   "IPTV.txt", "IPTV1_list.txt", "hubei.txt"]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
