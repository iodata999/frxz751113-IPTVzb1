import os
import requests
import re
import base64
import cv2
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# 获取rtp目录下的文件名
files = os.listdir('rtp')

files_name = []

# 去除后缀名并保存至provinces_isps
for file in files:
    name, extension = os.path.splitext(file)
    files_name.append(name)

#忽略不符合要求的文件名
provinces_isps = [name for name in files_name if name.count('_') == 1]

# 打印结果
print(f"本次查询：{provinces_isps}的组播节目") 

keywords = []

for province_isp in provinces_isps:
    # 读取文件并删除空白行
    try:
        with open(f'rtp/{province_isp}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]
        # 获取第一行中以包含 "rtp://" 的值作为 mcast
        if lines:
            first_line = lines[0]
            if "rtp://" in first_line:
                mcast = first_line.split("rtp://")[1].split(" ")[0]
                keywords.append(province_isp + "_" + mcast)
    except FileNotFoundError:
    # 如果文件不存在，则捕获 FileNotFoundError 异常并打印提示信息
        print(f"文件 '{province_isp}.txt' 不存在. 跳过此文件.")

for keyword in keywords:
    province, isp, mcast = keyword.split("_")
    #将省份转成英文小写
    # 根据不同的 isp 设置不同的 org 值
    if province == "北京" and isp == "联通":
        isp_en = "cucc"
        org = "China Unicom Beijing Province Network"
    elif isp == "联通":
        isp_en = "cucc"
        org = "CHINA UNICOM China169 Backbone"
    elif isp == "电信":
        org = "Chinanet"
        isp_en = "ctcc"
    elif isp == "移动":
        org == "China Mobile communications corporation"
        isp_en = "cmcc"
        
#    else:
#        org = ""

    current_time = datetime.now()
    timeout_cnt = 0
    result_urls = set() 
    while len(result_urls) == 0 and timeout_cnt <= 5:
        try:
            search_url = 'https://fofa.info/result?qbase64='
            search_txt = f'\"udpxy\" && country=\"CN\" && region=\"{province}\" && org=\"{org}\"'
                # 将字符串编码为字节流
            bytes_string = search_txt.encode('utf-8')
                # 使用 base64 进行编码
            search_txt = base64.b64encode(bytes_string).decode('utf-8')
            search_url += search_txt
            print(f"{current_time} 查询运营商 : {province}{isp} ，查询网址 : {search_url}")
            response = requests.get(search_url, timeout=30)
            # 处理响应
            response.raise_for_status()
            # 检查请求是否成功
            html_content = response.text
            # 使用BeautifulSoup解析网页内容
            html_soup = BeautifulSoup(html_content, "html.parser")
            # print(f"{current_time} html_content:{html_content}")
            # 查找所有符合指定格式的网址
            # 设置匹配的格式，如http://8.8.8.8:8888
            pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
            urls_all = re.findall(pattern, html_content)
            # 去重得到唯一的URL列表
            result_urls = set(urls_all)
            print(f"{current_time} result_urls:{result_urls}")

            valid_ips = []

            # 遍历所有视频链接
            for url in result_urls:
                video_url = url + "/rtp/" + mcast

                # 用OpenCV读取视频
                cap = cv2.VideoCapture(video_url)

                # 检查视频是否成功打开
                if not cap.isOpened():
                    print(f"{current_time} {video_url} 无效")
                else:
                    # 读取视频的宽度和高度
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    print(f"{current_time} {video_url} 的分辨率为 {width}x{height}")
                    # 检查分辨率是否大于0
                    if width > 0 and height > 0:
                        valid_ips.append(url)
                    # 关闭视频流
                    cap.release()
                    
            if valid_ips:
                #生成节目列表 省份运营商.txt
                rtp_filename = f'rtp/{province}_{isp}.txt'
                with open(rtp_filename, 'r', encoding='utf-8') as file:
                    data = file.read()
                txt_filename = f'{province}{isp}.txt'
                with open(txt_filename, 'w') as new_file:
                    for url in valid_ips:
                        new_data = data.replace("rtp://", f"{url}/rtp/")
                        new_file.write(new_data)

                print(f'已生成播放列表，保存至{txt_filename}')
                group_title = ""
                group_cctv = ["CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV5", "CCTV5+", "CCTV6", "CCTV7", "CCTV8", "CCTV9", "CCTV10", "CCTV11", "CCTV12", "CCTV13", "CCTV14", "CCTV15", "CCTV16", "CCTV17", "CCTV4K", "CCTV8K", "CGTN英语", "CGTN记录", "CGTN俄语", "CGTN法语", "CGTN西语", "CGTN阿语"]
                group_shuzi = ["CHC动作电影", "CHC家庭影院", "CHC高清电影", "重温经典", "第一剧场", "风云剧场", "怀旧剧场", "世界地理", "发现之旅", "求索纪录", "兵器科技", "风云音乐", "文化精品", "央视台球", "高尔夫网球", "风云足球", "女性时尚", "电视指南", "中视购物", "中学生", "卫生健康", "央广购物", "家有购物", "老故事", "书画", "中国天气", "收藏天下", "国学频道", "快乐垂钓", "先锋乒羽", "风尚购物", "财富天下", "天元围棋", "摄影频道", "新动漫", "证券服务", "梨园", "置业", "家庭理财", "茶友"]
                group_jiaoyu = ["CETV1", "CETV2", "CETV3", "CETV4", "山东教育", "早期教育"]
                group_weishi = ["北京卫视", "湖南卫视", "东方卫视", "四川卫视", "天津卫视", "安徽卫视", "山东卫视", "广东卫视", "广西卫视", "江苏卫视", "江西卫视", "河北卫视", "河南卫视", "浙江卫视", "海南卫视", "深圳卫视", "湖北卫视", "山西卫视", "东南卫视", "贵州卫视", "辽宁卫视", "重庆卫视", "黑龙江卫视", "内蒙古卫视", "宁夏卫视", "陕西卫视", "甘肃卫视", "吉林卫视", "云南卫视", "三沙卫视", "青海卫视", "新疆卫视", "西藏卫视", "兵团卫视", "延边卫视", "大湾区卫视", "安多卫视", "厦门卫视", "农林卫视", "康巴卫视", "优漫卡通", "哈哈炫动", "嘉佳卡通"]

                #生成m3u
                with open(txt_filename, 'r') as input_file:
                    lines = input_file.readlines()
                #删除空白行
                    lines = [line for line in lines if line.count(',') == 1]
                # 转换格式并写入到 省份运营商.m3u
                m3u_filename = f'{province}{isp}.m3u'
                with open(m3u_filename, 'w', encoding='utf-8') as output_file:
                    output_file.write('#EXTM3U  x-tvg-url="https://live.fanmingming.com/e.xml\n')  # 添加 #EXTM3U
                    for line in lines:
                        parts = line.strip().split(',')
                        name1 = parts[0]
                        uppercase_name1 = name1.upper()
                        name1 = uppercase_name1
                        name1 = name1.replace("中央", "CCTV")
                        name1 = name1.replace("高清", "")
                        name1 = name1.replace("HD", "")
                        name1 = name1.replace("标清", "")
                        name1 = name1.replace("频道", "")
                        name1 = name1.replace("-", "")
                        name1 = name1.replace("_", "")
                        name1 = name1.replace(" ", "")
                        name1 = name1.replace("PLUS", "+")
                        name1 = name1.replace("＋", "+")
                        name1 = name1.replace("(", "")
                        name1 = name1.replace(")", "")
                        name1 = name1.replace("CCTV1综合", "CCTV1")
                        name1 = name1.replace("CCTV2财经", "CCTV2")
                        name1 = name1.replace("CCTV3综艺", "CCTV3")
                        name1 = name1.replace("CCTV4国际", "CCTV4")
                        name1 = name1.replace("CCTV4中文国际", "CCTV4")
                        name1 = name1.replace("CCTV5体育", "CCTV5")
                        name1 = name1.replace("CCTV6电影", "CCTV6")
                        name1 = name1.replace("CCTV7军事", "CCTV7")
                        name1 = name1.replace("CCTV7军农", "CCTV7")
                        name1 = name1.replace("CCTV7国防军事", "CCTV7")
                        name1 = name1.replace("CCTV8电视剧", "CCTV8")
                        name1 = name1.replace("CCTV9记录", "CCTV9")
                        name1 = name1.replace("CCTV9纪录", "CCTV9")
                        name1 = name1.replace("CCTV10科教", "CCTV10")
                        name1 = name1.replace("CCTV11戏曲", "CCTV11")
                        name1 = name1.replace("CCTV12社会与法", "CCTV12")
                        name1 = name1.replace("CCTV13新闻", "CCTV13")
                        name1 = name1.replace("CCTV新闻", "CCTV13")
                        name1 = name1.replace("CCTV14少儿", "CCTV14")
                        name1 = name1.replace("CCTV15音乐", "CCTV15")
                        name1 = name1.replace("CCTV16奥林匹克", "CCTV16")
                        name1 = name1.replace("CCTV17农业农村", "CCTV17")
                        name1 = name1.replace("CCTV5+体育赛视", "CCTV5+")
                        name1 = name1.replace("CCTV5+体育赛事", "CCTV5+")
                        name1 = name1.replace("综合教育", "")
                        name1 = name1.replace("空中课堂", "")
                        name1 = name1.replace("教育服务", "")
                        name1 = name1.replace("职业教育", "")
                        name1 = name1.replace("Documentary", "记录")
                        name1 = name1.replace("Français", "法语")
                        name1 = name1.replace("Русский", "俄语")
                        name1 = name1.replace("Español", "西语")
                        name1 = name1.replace("العربية", "阿语")
                        name1 = name1.replace("NewTv", "")
                        name1 = name1.replace("CCTV兵器科技", "兵器科技")
                        name1 = name1.replace("CCTV怀旧剧场", "怀旧剧场")
                        name1 = name1.replace("CCTV世界地理", "世界地理")
                        name1 = name1.replace("CCTV文化精品", "文化精品")
                        name1 = name1.replace("CCTV央视台球", "央视台球")
                        name1 = name1.replace("CCTV央视高网", "央视高网")
                        name1 = name1.replace("CCTV风云剧场", "风云剧场")
                        name1 = name1.replace("CCTV第一剧场", "第一剧场")
                        name1 = name1.replace("CCTV风云足球", "风云足球")
                        name1 = name1.replace("CCTV电视指南", "电视指南")
                        name1 = name1.replace("CCTV风云音乐", "风云音乐")
                        name1 = name1.replace("CCTV女性时尚", "女性时尚")
                        name1 = name1.replace("CHC电影", "CHC高清电影")
                        name2 = parts[0]
                        url = parts[1]
                        if name1 in group_cctv:
                            group_title = "央视频道"
                        elif name1 in group_shuzi:
                            group_title = "数字频道"
                        elif name1 in group_jiaoyu:
                            group_title = "教育频道"
                        elif name1 in group_weishi:
                            group_title = "卫视频道"
                        else:
                            group_title = "其他频道"

                        output_file.write(f'#EXTINF:-1 tvg-id="{name1}" tvg-name="{name1}" tvg-logo="https://live.fanmingming.com/tv/{name1}.png" group-title="{group_title}",{name2}\n{url}\n')
        
                print(f'已保存至{m3u_filename}')

            else:
                print("未找到合适的 IP 地址。")

        except (requests.Timeout, requests.RequestException) as e:
            timeout_cnt += 1
            print(f"{current_time} [{province}]搜索请求发生超时，异常次数：{timeout_cnt}")
            if timeout_cnt <= 5:
                    # 继续下一次循环迭代
                continue
            else:
                print(f"{current_time} 搜索IPTV频道源[]，超时次数过多：{timeout_cnt} 次，停止处理")
print('节目表制作完成！ 文件输出在当前文件夹！')

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
from opencc import OpenCC
# 合并自定义频道文件#################################################################################################
# 合并自定义频道文件#################################################################################################
file_contents = []
file_paths = ["四川电信.txt", "广东电信.txt", "天津联通.txt", "江苏电信.txt", "湖北电信.txt", "河北电信.txt", "湖南电信.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("临时组播.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    


#替换多余的关键字词###################################################################################################
for line in fileinput.input("临时组播.txt", inplace=True):  #打开文件，并对其进行原地替换
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
    line = line.replace("熊猫影院", "熊猫电影")
    line = line.replace("熊猫爱生活", "熊猫生活")
    line = line.replace("爱宠宠物", "宠物生活")
    
    line = line.replace("CCTV10", "CCTW10")
    line = line.replace("CCTV11", "CCTW11")
    line = line.replace("CCTV12", "CCTW12")
    line = line.replace("CCTV13", "CCTW13")
    line = line.replace("CCTV14", "CCTW14")
    line = line.replace("CCTV15", "CCTW15")
    line = line.replace("CCTV16", "CCTW16")
    line = line.replace("CCTV17", "CCTW17")
    #需要排在前面的频道
    line = line.replace("湖南卫视", "一一湖南卫视")
    line = line.replace("湖北卫视", "一一湖北卫视")
    line = line.replace("江苏卫视", "一江苏卫视")
    line = line.replace("安徽卫视", "一安徽卫视")
    line = line.replace("第一", "一第一")
    line = line.replace("风云", "一风云")
    line = line.replace("都市", "一都市")
    line = line.replace("谍战", "一谍战")
    line = line.replace("热门", "一热门")
    
    
    line = line.replace("专区", "")
    line = line.replace("卫视超", "卫视")
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
    line = line.replace("CCTV4K测试）", "CCTV4K")
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
    line = line.replace("CCTV世界地理", "世界地理")
    line = line.replace("BTV北京卫视", "北京卫视")
    line = line.replace("BTV冬奥纪实", "冬奥纪实")
    line = line.replace("东奥纪实", "冬奥纪实")
    line = line.replace("卫视台", "卫视")
    line = line.replace("湖南电视台", "湖南卫视")
    line = line.replace("少儿科教", "少儿")
    line = line.replace("影视剧", "影视")
    line = line.replace("电视剧", "影视")
    line = line.replace("CCTV1CCTV1", "CCTV1")
    line = line.replace("CCTV2CCTV2", "CCTV2")
    line = line.replace("CCTV7CCTV7", "CCTV7")
    line = line.replace("CCTV10CCTV10", "CCTV10")
    print(line, end="")  #设置end=""，避免输出多余的换行符



#二次替换某些关键词为便于合并的自定义词####################################################################################################
for line in fileinput.input("临时组播.txt", inplace=True):  #打开文件，并对其进行原地替换
    
    line = line.replace("CCTV10", "CCTW10")
    line = line.replace("CCTV11", "CCTW11")
    line = line.replace("CCTV12", "CCTW12")
    line = line.replace("CCTV13", "CCTW13")
    line = line.replace("CCTV14", "CCTW14")
    line = line.replace("CCTV15", "CCTW15")
    line = line.replace("CCTV16", "CCTW16")
    line = line.replace("CCTV17", "CCTW17")
    #需要排在前面的频道
    line = line.replace("湖南卫视", "一一湖南卫视")
    line = line.replace("湖北卫视", "一一湖北卫视")
    line = line.replace("江苏卫视", "一江苏卫视")
    line = line.replace("安徽卫视", "一安徽卫视")
    line = line.replace("第一", "一第一")
    line = line.replace("风云", "一风云")
    line = line.replace("都市", "一都市")
    line = line.replace("谍战", "一谍战")
    line = line.replace("热门", "一热门")
    line = line.replace("专区", "")
    line = line.replace("卫视超", "卫视")
    line = line.replace("IPTV", "")
    line = line.replace("东奥纪实", "冬奥纪实")
    line = line.replace("卫视台", "卫视")
    line = line.replace("湖南电视台", "湖南卫视")
    line = line.replace("少儿科教", "少儿")
    line = line.replace("影视剧", "影视")
    line = line.replace("电视剧", "影视")
    line = line.replace("CCTV1CCTV1", "CCTV1")
    line = line.replace("CCTV2CCTV2", "CCTV2")
    line = line.replace("CCTV7CCTV7", "CCTV7")
    line = line.replace("CCTV10CCTV10", "CCTV10")
    print(line, end="")  #设置end=""，避免输出多余的换行符




#再次替换自定义词为常规词##########################################################################################################################
for line in fileinput.input("临时组播.txt", inplace=True):  #打开文件，并对其进行原地替换
    line = line.replace("CCTW10", "CCTV10")
    line = line.replace("CCTW11", "CCTV11")
    line = line.replace("CCTW12", "CCTV12")
    line = line.replace("CCTW13", "CCTV13")
    line = line.replace("CCTW14", "CCTV14")
    line = line.replace("CCTW15", "CCTV15")
    line = line.replace("CCTW16", "CCTV16")
    line = line.replace("CCTW17", "CCTV17")
    line = line.replace("DCTW4K", "CCTV4K")
    line = line.replace("CCTV4K测试）", "CCTV4")
    line = line.replace("CCTV164K", "CCTV16 4K")
    line = line.replace("CCTV54K", "CCTV5 4K")
    line = line.replace("CCTV8K", "CCTV 8K")
    line = line.replace("CCTV4K", "CCTV 4K")
    line = line.replace("卫视台", "卫视")
    line = line.replace("iHOT", "")
    line = line.replace("一一", "")
    line = line.replace("CHC电影", "CHC高清电影")
    line = line.replace("影视剧", "影视")
    line = line.replace("电视剧", "影视")
    line = line.replace("淮北教育", "安徽CCTV ")
    line = line.replace("CCTV1CCTV1", "CCTV1")
    line = line.replace("CCTV2CCTV2", "CCTV2")
    line = line.replace("CCTV7CCTV7", "CCTV7")
    line = line.replace("CCTV10CCTV10", "CCTV10")
    line = line.replace("高清电影", "影迷电影")
    print(line, end="")  #设置end=""，避免输出多余的换行符


#从整理好的文本中按类别进行特定关键词提取#############################################################################################
keywords = ['环绕']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n高质组播,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
for line in fileinput.input("c.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("综合文艺", "")                                                                         ###########                                                      ###########
    line = line.replace("科教", "")                                                                         ###########                                                      ###########
    line = line.replace("社会与法", "")                                                                         ###########                                                      ###########
    line = line.replace("新闻", "")                                                                         ###########                                                      ###########
    line = line.replace("少儿", "")                                                                         ###########                                                      ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("地理世界", "世界地理")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符          

#从整理好的文本中按类别进行特定关键词提取#############################################################################################
keywords = ['CCTV']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('c1.txt', 'w', encoding='utf-8') as c1:    #####定义临时文件名
    c1.write('央视系列,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c1.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
for line in fileinput.input("c1.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("综合文艺", "")                                                                         ###########                                                      ###########
    line = line.replace("科教", "")                                                                         ###########                                                      ###########
    line = line.replace("社会与法", "")                                                                         ###########                                                      ###########
    line = line.replace("新闻", "")                                                                         ###########                                                      ###########
    line = line.replace("少儿", "")                                                                         ###########                                                      ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("地理世界", "世界地理")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符          




keywords = ['风云', '兵器', '女性', '地理', '央视文化', '风云', '怀旧剧场', '第一剧场', 'CHC']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('e.txt', 'w', encoding='utf-8') as e:    #####定义临时文件名
    e.write('\n高质组播,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if '环绕' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         e.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
for line in fileinput.input("e.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("综合文艺", "")                                                                         ###########                                                      ###########
    line = line.replace("科教", "")                                                                         ###########                                                      ###########
    line = line.replace("社会与法", "")                                                                         ###########                                                      ###########
    line = line.replace("新闻", "")                                                                         ###########                                                      ###########
    line = line.replace("少儿", "")                                                                         ###########                                                      ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("地理世界", "世界地理")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符          

keywords = ['卫视']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('e1.txt', 'w', encoding='utf-8') as e1:    #####定义临时文件名
    e1.write('\n卫视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if '环绕' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         e1.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
for line in fileinput.input("e1.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("综合文艺", "")                                                                         ###########                                                      ###########
    line = line.replace("科教", "")                                                                         ###########                                                      ###########
    line = line.replace("社会与法", "")                                                                         ###########                                                      ###########
    line = line.replace("新闻", "")                                                                         ###########                                                      ###########
    line = line.replace("少儿", "")                                                                         ###########                                                      ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    line = line.replace("地理世界", "世界地理")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符          



###############################################################################################################################################################################
keywords = ['4K', '8K']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('DD.txt', 'w', encoding='utf-8') as DD:
    DD.write('\n4K 频道,#genre#\n')
    for line in file:
      if '环绕' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
          DD.write(line)  # 将该行写入输出文件

for line in fileinput.input("DD.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      




###############################################################################################################################################################################
keywords = ['湖南', '广东', '武汉', '湖北', '安徽', '天津', '广州', '河北']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('df.txt', 'w', encoding='utf-8') as df:
    df.write('\n省市频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line and '4K' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          df.write(line)  # 将该行写入输出文件
for line in fileinput.input("df.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      

###############################################################################################################################################################################
keywords = ['综合', '公共', '生活', '新闻', '电视', '文艺', '经济']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('临时组播.txt', 'r', encoding='utf-8') as file, open('xs.txt', 'w', encoding='utf-8') as xs:
    xs.write('\n地方频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line and '湖南' not in line and '广东' not in line and '湖北' not in line and '安徽' not in line and '天津' not in line and '河北' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          xs.write(line)  # 将该行写入输出文件
for line in fileinput.input("xs.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      



######################################################################################################################打开欲要最终合并的文件并输出临时文件并替换关键词
with open('酒店源.txt', 'r', encoding='utf-8') as f:  #打开文件，并对其进行关键词提取                                               ###########
 keywords = ['http', 'rtmp', 'genre']  # 需要提取的关键字列表                                                       ###########
 #keywords = ['CCTV', '卫视', 'http', '重温', '酒店', '私人', '天映', '莲花', 'AXN', '好莱坞', '星', '龙', '凤凰', '东森', 'genre']  # 需要提取的关键字列表                                                       ###########
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字                                      ###########
 #pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制                                                     ###########
 with open('酒店源.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:           ###########
    #b.write('\n央视频道,#genre#\n')                                                                        ###########
    for line in file:                                                                                      ###########
        if re.search(pattern, line):  # 如果行中有任意关键字                                                ###########
          b.write(line)  # 将该行写入输出文件                                                               ###########
                                                                                                           ###########
for line in fileinput.input("b.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    #line = line.replace("央视频道,#genre#", "")                                                                         ###########
    line = line.replace("四川康巴卫视", "康巴卫视")                                                                         ###########
    line = line.replace("黑龙江卫视+", "黑龙江卫视")                                                                         ###########
    line = line.replace("[1920*1080]", "")                                                                         ###########
    line = line.replace("湖北电视台", "湖北综合")                                                                         ###########
    line = line.replace("教育台", "教育")                                                                         ###########
    line = line.replace("星河", "TVB星河")                                                        ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符   
    

######################################################################################################################打开欲要最终合并的文件并输出临时文件并替换关键词
with open('光迅源.txt', 'r', encoding='utf-8') as f:  #打开文件，并对其进行关键词提取                                               ###########
 keywords = ['http', 'rtmp', 'genre']  # 需要提取的关键字列表                                                       ###########
 #keywords = ['CCTV', '卫视', 'http', '重温', '酒店', '私人', '天映', '莲花', 'AXN', '好莱坞', '星', '龙', '凤凰', '东森', 'genre']  # 需要提取的关键字列表                                                       ###########
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字                                      ###########
 #pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制                                                     ###########
 with open('光迅源.txt', 'r', encoding='utf-8') as file, open('d.txt', 'w', encoding='utf-8') as d:           ###########
    #b.write('\n央视频道,#genre#\n')                                                                        ###########
    for line in file:                                                                                      ###########
        if re.search(pattern, line):  # 如果行中有任意关键字                                                ###########
          d.write(line)  # 将该行写入输出文件     


##############################################################################################################################################################################################################################################

#  获取远程港澳台直播源文件，打开文件并输出临时文件并替换关键词
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/TW.txt"          #源采集地址
r = requests.get(url)
open('TW.txt','wb').write(r.content)         #打开源文件并临时写入
#keywords = ['http', 'rtmp']  # 需要提取的关键字列表 8M1080
#pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
pattern = r"^(.*?),(?!#genre#)(.*?)$" #直接复制不带分类行
with open('TW.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:
    a.write('\n港澳频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          a.write(line)  # 将该行写入输出文件
for line in fileinput.input("a.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("﻿Taiwan,#genre#", "")                         #编辑替换字
    line = line.replace("﻿amc", "AMC")                         #编辑替换字
    line = line.replace("﻿中文台", "中文")                         #编辑替换字
    print(line, end="")                                     #加入此行去掉多余的转行符



        


###########################################################################################################################################################################
# 读取要合并的频道文件，并生成临时文件##############################################################################################################
file_contents = []
file_paths = ["b.txt", "d.txt", "a.txt", "c.txt", "e.txt", "DD.txt", "df.txt", "xs.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

           

 ###########################################################################################################################################################################     
# 读取临时文件，并生成结果文件。这一步其实多余，懒得改##############################################################################################################
file_contents = []
file_paths = ["GAT.txt"]  # 替换为实际的文件路径列表


for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
###########################################################################################################################################################################
# 写入合并后的文件
with open("综合源.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

for line in fileinput.input("综合源.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("CCTV1,", "CCTV1-综合,")  
    line = line.replace("CCTV2,", "CCTV2-财经,")  
    line = line.replace("CCTV3,", "CCTV3-综艺,")  
    line = line.replace("CCTV4,", "CCTV4-国际,")  
    line = line.replace("CCTV5,", "CCTV5-体育,")  
    line = line.replace("CCTV5+,", "CCTV5-体育plus,")  
    line = line.replace("CCTV6,", "CCTV6-电影,")  
    line = line.replace("CCTV7,", "CCTV7-军事,")  
    line = line.replace("CCTV8,", "CCTV8-电视剧,")  
    line = line.replace("CCTV9,", "CCTV9-纪录,")  
    line = line.replace("CCTV10,", "CCTV10-科教,")  
    line = line.replace("CCTV11,", "CCTV11-戏曲,")  
    line = line.replace("CCTV11+,", "CCTV11-戏曲,")  
    line = line.replace("CCTV12,", "CCTV12-社会与法,")  
    line = line.replace("CCTV13,", "CCTV13-新闻,")  
    line = line.replace("CCTV14,", "CCTV14-少儿,")  
    line = line.replace("CCTV15,", "CCTV15-音乐,")  
    line = line.replace("CCTV16,", "CCTV16-奥林匹克,")  
    line = line.replace("CCTV17,", "CCTV17-农业农村,") 
    line = line.replace("CCTV风", "风")  
    line = line.replace("CCTV兵", "兵")  
    line = line.replace("CCTV世", "世")  
    line = line.replace("CCTV女", "女")  
    line = line.replace("008广", "广")
    line = line.replace("家庭电影", "家庭影院")    
    line = line.replace("CHC", "")  
    line = line.replace("科技生活", "科技")  
    line = line.replace("财经生活", "财经")  
    line = line.replace("新闻综合", "新闻")  
    line = line.replace("公共新闻", "公共")  
    line = line.replace("经济生活", "经济")  
    line = line.replace("频道1", "频道")  
    print(line, end="")   

###########################################################################################################################################################################
# 读取要合并的频道文件，并生成临时文件##############################################################################################################
file_contents = []
file_paths = ["c1.txt", "e.txt", "e1.txt", "DD.txt", "df.txt", "xs.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT1.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

           

 ###########################################################################################################################################################################     
# 读取临时文件，并生成结果文件。这一步其实多余，懒得改##############################################################################################################
file_contents = []
file_paths = ["GAT1.txt"]  # 替换为实际的文件路径列表


for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
###########################################################################################################################################################################
# 写入合并后的文件
with open("组播源.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
for line in fileinput.input("综合源.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("高质组播", "央视系列")    
    print(line, end="")   


################简体转繁体
# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('综合源.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入txt文件
with open('综合源.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)

######################TXT转M3U#####################################################################################################################################################
def txt_to_m3u(input_file, output_file):
    # 读取txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打开m3u文件并写入内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"\n')
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
                    f.write(f'#EXTINF:-1 tvg-logo="https://live.fanmingming.com/tv/{channel_name}.png" group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')


# 将txt文件转换为m3u文件
txt_to_m3u('综合源.txt', '综合源.m3u')




"四川电信.txt", "广东电信.txt", "天津联通.txt", "江苏电信.txt", "湖北电信.txt", "河北电信.txt", "湖南电信.txt"
###########################################################################################################################################################################
#任务结束，删除不必要的过程文件###########################################################################################################################
os.remove("GAT.txt")
os.remove("DD.txt")
os.remove("TW.txt")
os.remove("a.txt")
os.remove("b.txt")
os.remove("c.txt")
os.remove("e.txt")
os.remove("c1.txt")
os.remove("e1.txt")
os.remove("d.txt")
os.remove("df.txt")
os.remove("d.txt")
os.remove("临时组播.txt")
os.remove("四川电信.txt")
os.remove("广东电信.txt")
os.remove("天津联通.txt")
os.remove("江苏电信.txt")
os.remove("湖北电信.txt")
os.remove("安徽电信.txt")
os.remove("河北电信.txt")
os.remove("湖南电信.txt")
os.remove("四川电信.m3u")
os.remove("广东电信.m3u")
os.remove("天津联通.m3u")
os.remove("江苏电信.m3u")
os.remove("湖北电信.m3u")
os.remove("河北电信.m3u")
os.remove("湖南电信.m3u")
os.remove("安徽电信.m3u")
print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")
