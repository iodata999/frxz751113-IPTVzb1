
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

url = "https://raw.githubusercontent.com/frxz751113/IPTVzb1/main/合并.txt"          #源采集地址
r = requests.get(url)
open('合并.txt','wb').write(r.content)         #打开源文件


for line in fileinput.input("合并.txt", inplace=True):  #打开文件，并对其进行原地替换
    line = line.replace("CCTV-1高清测试", "")
    line = line.replace("CCTV-2高清测试", "")
    line = line.replace("CCTV-7高清测试", "")
    line = line.replace("CCTV-10高清测试", "")
    line = line.replace("中央", "CCTV")
    line = line.replace("高清", "")
    line = line.replace("HD", "")
    line = line.replace("标清", "")
    line = line.replace("超清", "")
    line = line.replace("频道", "")
    line = line.replace("-", "")
    line = line.replace(" ", "")
    line = line.replace("CCTV风云剧场", "风云剧场")
    line = line.replace("CCTV第一剧场", "第一剧场")
    line = line.replace("CCTV怀旧剧场", "怀旧剧场")
    line = line.replace("IPTV", "")
    line = line.replace("PLUS", "+")
    line = line.replace("＋", "+")
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("CAV", "")
    line = line.replace("美洲", "")
    line = line.replace("北美", "")
    line = line.replace("12M", "")
    line = line.replace("高清测试(CCTV-1", "")
    line = line.replace("高清测试(CCTV-2", "")
    line = line.replace("高清测试(CCTV-7", "")
    line = line.replace("高清测试(CCTV-10", "")
    line = line.replace("LD", "")
    line = line.replace("HEVC20M", "")
    line = line.replace("测试001", "TVB星河")
    line = line.replace("测试002", "凤凰卫视")
    line = line.replace("测试003", "凤凰卫视")
    line = line.replace("测试004", "私人影院")
    line = line.replace("测试005", "私人影院")
    line = line.replace("测试006", "东森洋片")
    line = line.replace("测试007", "东森电影")
    line = line.replace("测试008", "AXN电影")
    line = line.replace("测试009", "好莱坞电影")
    line = line.replace("测试010", "龙祥电影")
    line = line.replace("测试016", "澳门莲花")
    line = line.replace("测试011", "凤凰香港")
    line = line.replace("S,", ",")
    line = line.replace("测试", "")
    line = line.replace("试看", "")
    line = line.replace("测试", "")
    line = line.replace("测试cctv", "CCTV")
    line = line.replace("CCTV1综合", "CCTV1")
    line = line.replace("CCTV2财经", "CCTV2")
    line = line.replace("CCTV3综艺", "CCTV3")
    line = line.replace("CCTV4国际", "CCTV4")
    line = line.replace("CCTV4中文国际", "CCTV4")
    line = line.replace("CCTV4欧洲", "CCTV4")
    line = line.replace("CCTV5体育", "CCTV5")
    line = line.replace("CCTV5+体育", "CCTV5+")
    line = line.replace("CCTV6电影", "CCTV6")
    line = line.replace("CCTV7军事", "CCTV7")
    line = line.replace("CCTV7军农", "CCTV7")
    line = line.replace("CCTV7农业", "CCTV7")
    line = line.replace("CCTV7国防军事", "CCTV7")
    line = line.replace("CCTV8电视剧", "CCTV8")
    line = line.replace("CCTV8纪录", "CCTV9")
    line = line.replace("CCTV9记录", "CCTV9")
    line = line.replace("CCTV9纪录", "CCTV9")
    line = line.replace("CCTV10科教", "CCTV10")
    line = line.replace("CCTV11戏曲", "CCTV11")
    line = line.replace("CCTV12社会与法", "CCTV12")
    line = line.replace("CCTV13新闻", "CCTV13")
    line = line.replace("CCTV新闻", "CCTV13")
    line = line.replace("CCTV14少儿", "CCTV14")
    line = line.replace("央视14少儿", "CCTV14")
    line = line.replace("CCTV少儿超", "CCTV14")
    line = line.replace("CCTV15音乐", "CCTV15")
    line = line.replace("CCTV音乐", "CCTV15")
    line = line.replace("CCTV16奥林匹克", "CCTV16")
    line = line.replace("CCTV17农业农村", "CCTV17")
    line = line.replace("CCTV17军农", "CCTV17")
    line = line.replace("CCTV17农业", "CCTV17")
    line = line.replace("CCTV5+体育赛视", "CCTV5+")
    line = line.replace("CCTV5+赛视", "CCTV5+")
    line = line.replace("CCTV5+体育赛事", "CCTV5+")
    line = line.replace("CCTV5+赛事", "CCTV5+")
    line = line.replace("CCTV5+体育", "CCTV5+")
    line = line.replace("CCTV5赛事", "CCTV5+")
    line = line.replace("凤凰中文台", "凤凰中文")
    line = line.replace("凤凰资讯台", "凤凰资讯")
    line = line.replace("CCTV4K测试）", "CCTV4")
    line = line.replace("CCTV164K", "CCTV16")
    line = line.replace("上海东方卫视", "上海卫视")
    line = line.replace("东方卫视", "上海卫视")
    line = line.replace("内蒙卫视", "内蒙古卫视")
    line = line.replace("福建东南卫视", "东南卫视")
    line = line.replace("广东南方卫视", "南方卫视")
    line = line.replace("湖南金鹰卡通", "金鹰卡通")
    line = line.replace("炫动卡通", "哈哈炫动")
    line = line.replace("卡酷卡通", "卡酷少儿")
    line = line.replace("卡酷动画", "卡酷少儿")
    line = line.replace("BRTVKAKU少儿", "卡酷少儿")
    line = line.replace("优曼卡通", "优漫卡通")
    line = line.replace("优曼卡通", "优漫卡通")
    line = line.replace("嘉佳卡通", "佳嘉卡通")
    line = line.replace("世界地理", "地理世界")
    line = line.replace("CCTV世界地理", "地理世界")
    line = line.replace("BTV北京卫视", "北京卫视")
    line = line.replace("BTV冬奥纪实", "冬奥纪实")
    line = line.replace("东奥纪实", "冬奥纪实")
    line = line.replace("卫视台", "卫视")
    line = line.replace("湖南电视台", "湖南卫视")
    line = line.replace("少儿科教", "少儿")
    line = line.replace("TV星河2）", "星河")
    line = line.replace("影视剧", "影视")
    line = line.replace("电视剧", "影视")
    line = line.replace("卡", "")
    line = line.replace("CCTV1CCTV1", "CCTV1")
    line = line.replace("CCTV2CCTV2", "CCTV2")
    line = line.replace("CCTV7CCTV7", "CCTV7")
    line = line.replace("CCTV10CCTV10", "CCTV10")
    print(line, end="")  #设置end=""，避免输出多余的换行符


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
with open("结果.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

# 写入更新日期时间
    #now = datetime.now()
    #output.write(f"更新时间,#genre#\n")
    #output.write(f"{now.strftime("%Y-%m-%d")},url\n")
    #output.write(f"{now.strftime("%H:%M:%S")},url\n")

os.remove("合并.txt")
os.remove("GAT.txt")
os.remove("ws.txt")
os.remove("df.txt")
#os.remove("DIYP-v4.txt")
os.remove("TW.txt")
print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")
