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

#  获取远程港澳台直播源文件
url = "https://raw.gitcode.com/frxz751113/1/raw/main/IPTV/ott移动v4.txt"          #源采集地址
r = requests.get(url)
open('ott移动v4.txt','wb').write(r.content)         #打开源文件并临时写入

keywords = [',']  # 需要提取的关键字列表 8M1080
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('ott移动v4.txt', 'r', encoding='utf-8') as file, open('TW.txt', 'w', encoding='utf-8') as TW:
    #TW.write('\n央视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          TW.write(line)  # 将该行写入输出文件

# 读取要合并的香港频道和台湾频道文件
file_contents = []
file_paths = ["TW.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))


# 扫源测绘空间地址
# 搜素关键词："iptv/live/zh_cn.js" && country="CN" && region="Hunan" && city="changsha"
# 搜素关键词："ZHGXTV" && country="CN" && region="Hunan" && city="changsha"
#"isShowLoginJs"智能KUTV管理

urls = [
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODgwMCI%3D",#8800
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODg4MyI%3D",#8883
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iMTExMSI%3D",#1111
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iNzAwNCI%3D",#7004
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJoZWJlaSI%3D",#河北
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODg4OCI%3D",#8888
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODA5NiI%3D",#8096
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iOTk5OSI%3D",#9999
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iOTkwMSI%3D",#9901
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgb3JnPSJDaGluYW5ldCI%3D",#电信随机
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJIdW5hbiI%3D",#湖南
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJodWJlaSIgJiYgcG9ydD0iOTkwMSI%3D",  #湖北9901
    #"https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgIHJlZ2lvbj0iSHVuYW4iICYmIHBvcnQ9Ijk5MDEi",  #湖南9901
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODE4MSIgJiYgY2l0eT0iR3VpZ2FuZyI%3D",  #贵港8181
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0ieXVsaW4i",#玉林
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJIdWJlaSIg",#湖北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcG9ydD0iODE4MSI%3D",#8181
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgcmVnaW9uPSJIdWJlaSIgJiYgcG9ydD0iOTkwMCI%3D",  #湖北9000,已存活1年
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bm%2F6KW%2FIg%3D%3D",    #广西 壮族iptv
    "https://fofa.info/result?qbase64=ImlzU2hvd0xvZ2luSnMiICYmIHJlZ2lvbj0iSGVpbG9uZ2ppYW5nIg%3D%3D",  # Heilongjiang (黑龙江)
]
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
        response = requests.get(url, timeout=3)          ###//////////////////
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None


results = []

for url in urls:
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
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        #if '卡通' in channel_name or '少儿' in channel_name or '哈哈' in channel_name or '动漫' in channel_name:
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
file_paths = ["GAT.txt", "hn.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("酒店源.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
for line in fileinput.input("酒店源.txt", inplace=True):  #打开文件，并对其进行关键词原地替换 
    line = line.replace("AA", "")
    line = line.replace("\n电影,", "\n影迷电影,")
    print(line, end="")  #设置end=""，避免输出多余的换行符  

#########原始顺序去重，以避免同一个频道出现在不同的类中
with open('酒店源.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
# 使用列表来存储唯一的行的顺序 
 unique_lines = [] 
 seen_lines = set() 
# 遍历每一行，如果是新的就加入unique_lines 
for line in lines:
 if line not in seen_lines:
  unique_lines.append(line)
  seen_lines.add(line)
# 将唯一的行写入新的文档 
with open('酒店源.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)
#####################


os.remove("iptv.txt")
os.remove("GAT.txt")
os.remove("hn.txt")
#os.remove("HK.txt")
os.remove("TW.txt")
os.remove("ott移动v4.txt")
print("任务运行完毕")
