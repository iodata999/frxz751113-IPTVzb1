import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import re
import os
hb = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki"        #河北
gx = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bm%2F6KW%2FIg%3D%3D"   #广西
gg = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Imd1aWdhbmci"   #贵港
sx = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D"    #陕西
ln = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ibGlhb25pbmci"    #辽宁
fj = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D"    #福建
hn = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D"    #河南

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
results_1 = process_url(hb)
save_results(results_1, "hb.txt")



# 处理第2个URL
results_shanghai = process_url(gx)
save_results(results_shanghai, "gx.txt")

# 处理第3个URL
results_tianjin = process_url(gg)
save_results(results_tianjin, "gg.txt")

# 处理第4个URL
results_6 = process_url(ln)
save_results(results_6, "ln.txt")


# 处理第5个URL
results_5 = process_url(fj)
save_results(results_5, "fj.txt")


# 处理第6个URL
results_6 = process_url(sx)
save_results(results_6, "sx.txt")



# 处理第7个URL
results_7 = process_url(hn)
save_results(results_7, "hn.txt")

# 合并文件内容
file_contents = []
file_paths = ["hb.txt", "gx.txt", "gg.txt", "ln.txt", "fj.txt", "sx.txt", "hn.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("IPTV.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

import re
import requests
import concurrent.futures

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

# 将排序后的结果写入speed_results.txt文件
with open("IPTV_list.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}")

# 从speed_results.txt文件中读取有效的频道信息（即响应时间不为"Failed"）
channels = []
with open("IPTV_list.txt", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            channel_name, channel_url, speed = line.split(',')
            if speed != "Failed":
                channels.append((channel_name,channel_url))

# 对频道进行排序，关键字为频道名称中的数字
channels.sort(key=lambda x: channel_key(x[0]))

# 将排序后的频道信息写入IPTV_speed.txt文件
with open("IPTV_list.txt", 'w', encoding='utf-8') as file:
    for channel_name,channel_url in channels:
        file.write(f'{channel_name},{channel_url}')
os.remove("iptv.txt")
os.remove("hb.txt")
os.remove("gx.txt")
os.remove("gg.txt")
os.remove("ln.txt")
os.remove("fj.txt")
os.remove("sx.txt")
os.remove("hn.txt")
print("任务运行完毕")
