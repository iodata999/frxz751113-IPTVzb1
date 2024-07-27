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
            first_line = lines[1]
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

# 合并自定义频道文件#################################################################################################

file_contents = []
file_paths = ["四川电信.txt", "广东电信.txt", "湖南电信.txt", "河南电信.txt", "河北电信.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
    else:                # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file_path} 不存在，跳过")
# 写入合并后的文件
with open("组播源.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

for line in fileinput.input("组播源.txt", inplace=True):  #打开文件，并对其进行关键词原地替换 
    line = line.replace("CHC电影", "CHC影迷电影") 
    line = line.replace("高清电影", "影迷电影") 
    print(line, end="")  #设置end=""，避免输出多余的换行符   






#从整理好的文本中按类别进行特定关键词提取#############################################################################################
keywords = ['CHC', '峨眉', '华语', '星光院线', '剧场', '家庭', '影迷', '动作', '星空', '凤凰']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('c2.txt', 'w', encoding='utf-8') as c2:    #####定义临时文件名
    c2.write('\n组播剧场,#genre#\n')                                                                  #####写入临时文件名$GD
    for line in file:
      if '$GD' not in line and '调解' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c2.write(line)  # 将该行写入输出文件                                                          #####定义临时文件


#从整理好的文本中按类别进行特定关键词提取#############################################################################################
keywords = ['爱动漫', '爱怀旧', '爱经典', '爱科幻', '爱幼教', '爱青春', '爱院线', '爱悬疑']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('c1.txt', 'w', encoding='utf-8') as c1:    #####定义临时文件名
    c1.write('\niHOT系列,#genre#\n')                                                                  #####写入临时文件名$GD
    for line in file:
      if '$GD' not in line and '4K' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c1.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
 


###############################################################################################################################################################################
keywords = ['4K', '8K']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('DD.txt', 'w', encoding='utf-8') as DD:
    DD.write('\n4K 频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          DD.write(line)  # 将该行写入输出文件

keywords = ['湖南', '广东', '广州', '河南', '河北']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('df1.txt', 'w', encoding='utf-8') as df1:
    #df1.write('\n省市频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line and '4K' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          df1.write(line)  # 将该行写入输出文件





################
keywords = ['河北', '石家庄', '丰宁', '临漳', '井陉', '井陉矿区', '保定', '元氏', '兴隆', '内丘', '南宫', '吴桥', '唐县', '唐山', '安平', '定州', '大厂', '张家口', '徐水', '成安', \
            '承德', '故城', '康保', '廊坊', '晋州', '景县', '武安', '枣强', '柏乡', '涉县', '涞水', '涞源', '涿州', '深州', '深泽', '清河', '秦皇岛', '衡水', '遵化', '邢台', '邯郸', \
            '邱县', '隆化', '雄县', '阜平', '高碑店', '高邑', '魏县', '黄骅', '饶阳', '赵县', '睛彩河北', '滦南', '玉田', '崇礼', '平泉', '容城', '文安', '三河', '清河']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('f.txt', 'w', encoding='utf-8') as f:    #####定义临时文件名
    f.write('\n河北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f.write(line)  # 将该行写入输出文件


###############f1
keywords = ['河南', '焦作', '开封', '卢氏', '洛阳', '孟津', '安阳', '宝丰', '邓州', '渑池', '南阳', '内黄', '平顶山', '淇县', '郏县', '封丘', '获嘉', '巩义', '杞县', '汝阳', '三门峡', '卫辉', '淅川', \
            '新密', '新乡', '信阳', '新郑', '延津', '叶县', '义马', '永城', '禹州', '原阳', '镇平', '郑州', '周口']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('f1.txt', 'w', encoding='utf-8') as f1:    #####定义临时文件名
    f1.write('\n河南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f1.write(line)  # 将该行写入输出文件




