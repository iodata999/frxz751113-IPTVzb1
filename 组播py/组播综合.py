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
import base64
import cv2
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
            if timeout_cnt <= 3:
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
 
#从整理好的文本中按类别进行特定关键词提取#######################################################################################################################################
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
#从整理好的文本中按类别进行特定关键词提取#######################################################################################################################################
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
#从整理好的文本中按类别进行特定关键词提取#######################################################################################################################################
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
#从文本中截取省市段生成新文件#######################################################################################################################################
# 定义关键词
start_keyword = '省市频道,#genre#'
end_keyword = '其他频道,#genre#'
# 输入输出文件路径
input_file_path = '光迅源.txt'  # 替换为你的输入文件路径
output_file_path = 'df.txt'  # 替换为你想要保存输出的文件路径
# 用于存储结果的列表
result_lines = []
# 打开输入文件并读取内容
with open(input_file_path, 'r', encoding='utf-8') as file:
    capture = False  # 用于控制是否开始捕获行
    for line in file:
        # 检查是否到达开始关键词
        if start_keyword in line:
            capture = True
            result_lines.append(line)  # 添加开始关键词所在的行
        # 如果已经开始捕获，并且到达结束关键词，则停止捕获
        elif end_keyword in line and capture:
            break
        # 如果处于捕获状态，则添加当前行
        if capture:
            result_lines.append(line)
# 将结果写入输出文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(result_lines)
print('提取完成，结果已保存到:', output_file_path)
###############################################################################################################################################################################
###############################################################################################################################################################################
#  获取远程港澳台直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/TW.txt"          #源采集地址
r = requests.get(url)
open('港澳.txt','wb').write(r.content)         #打开源文件并临时写入



###############################################################################################################################################################################
#从整理好的文本中按类别进行特定关键词提取#######################################################################################################################################
with open('光迅源.txt', 'r', encoding='utf-8') as f:  #打开文件，并对其进行关键词提取                                               ###########
 #keywords = ['http', 'rtmp', 'genre']  # 需要提取的关键字列表                                                       ###########
 keywords = ['重温', '光迅', '私人', '天映', '莲花', 'AXN', '好莱坞', 'TVB', '星', '广场舞', '龙祥', '凤凰', '东森']  # 需要提取的关键字列表                                                       ###########
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字                                      ###########
 #pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制                                                     ###########
 with open('光迅源.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:           ###########
    b.write('\n光迅港澳,#genre#\n')                                                                        ###########
    for line in file:                                                                                      ###########
        if re.search(pattern, line):  # 如果行中有任意关键字                                                ###########
          b.write(line)  # 将该行写入输出文件                                                               ###########
                                                                                                           ##########################################################################################################################################################################################



#从整理好的文本中进行特定关键词替换以规范频道名#######################################################################################################################################
for line in fileinput.input("b.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    #line = line.replace("央视频道,#genre#", "")                                                                         ###########
    line = line.replace("四川康巴卫视", "康巴卫视")                                                                         ###########
    line = line.replace("黑龙江卫视+", "黑龙江卫视")                                                                         ###########
    line = line.replace("[1920*1080]", "")                                                                         ###########
    line = line.replace("湖北电视台", "湖北综合")                                                                         ###########
    line = line.replace("教育台", "教育")                                                                         ###########
    #line = line.replace("星河", "TVB星河")                                                        ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符   
    
###############################################################################################################################################################################
#从文本中截取少儿段生成新文件#######################################################################################################################################
# 定义关键词
start_keyword = '少儿频道,#genre#'
end_keyword = '省市频道,#genre#'
# 输入输出文件路径
input_file_path = '光迅源.txt'  # 替换为你的输入文件路径
output_file_path = 'sr2.txt'  # 替换为你想要保存输出的文件路径
# 用于存储结果的列表
result_lines = []
# 打开输入文件并读取内容
with open(input_file_path, 'r', encoding='utf-8') as file:
    capture = False  # 用于控制是否开始捕获行
    for line in file:
        # 检查是否到达开始关键词
        if start_keyword in line:
            capture = True
        # 如果已经开始捕获，并且到达结束关键词，则停止捕获
        elif end_keyword in line and capture:
            break
        # 如果处于捕获状态，则添加当前行
        if capture:
            result_lines.append(line)
# 将结果写入输出文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(result_lines)
print('提取完成，结果已保存到:', output_file_path)
############################################################################################################################################################################################################################################################################################################################################################################################################################
#从文本中截取省市段生成两个新文件#######################################################################################################################################
#  获取远程港澳台直播源文件，打开文件并输出临时文件并替换关键词
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/汇总.txt"          #源采集地址
r = requests.get(url)
open('TW.txt','wb').write(r.content)         #打开源文件并临时写入
for line in fileinput.input("TW.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("﻿Taiwan,#genre#", "")                         #编辑替换字
    line = line.replace("﻿amc", "AMC")                         #编辑替换字
    line = line.replace("﻿中文台", "中文")                         #编辑替换字
    print(line, end="")                                     #加入此行去掉多余的转行符
# 定义关键词
start_keyword = '省市频道,#genre#'
end_keyword = '港澳频道,#genre#'
# 输入输出文件路径
input_file_path = 'TW.txt'  # 替换为你的输入文件路径
output_file_path = 'a.txt'  # 替换为你想要保存输出的文件路径
deleted_lines_file_path = 'df0.txt'  # 替换为你想要保存删除行的文件路径
# 标记是否处于要删除的行范围内
delete_range = False
# 存储要删除的行，包括开始关键词行
deleted_lines = []
# 读取原始文件并过滤掉指定范围内的行
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 过滤掉不需要的行
filtered_lines = []
for line in lines:
    if start_keyword in line:
        delete_range = True
        deleted_lines.append(line)  # 将开始关键词行添加到删除行列表
        continue
    if delete_range:
        if end_keyword in line:
            delete_range = False
            filtered_lines.append(line)  # 将结束关键词行添加到输出文件列表
        else:
            deleted_lines.append(line)  # 添加到删除行列表
    else:
        filtered_lines.append(line)
# 将过滤后的内容写入新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)
# 将删除的行写入到新的文件中
with open(deleted_lines_file_path, 'w', encoding='utf-8') as file:
    file.writelines(deleted_lines)
print('过滤完成，结果已保存到:', output_file_path)
print('删除的行已保存到:', deleted_lines_file_path)


###############################################################################################################################################################################
#从文本中截取少儿段并生成两个新文件#######################################################################################################################################
# 定义关键词
start_keyword = '少儿频道,#genre#'
end_keyword = '港澳频道,#genre#'
# 输入输出文件路径
input_file_path = 'a.txt'  # 替换为你的输入文件路径
output_file_path = 'a0.txt'  # 替换为你想要保存输出的文件路径
deleted_lines_file_path = 'sr1.txt'  # 替换为你想要保存删除行的文件路径
# 标记是否处于要删除的行范围内
delete_range = False
# 存储要删除的行，包括开始关键词行
deleted_lines = []
# 读取原始文件并过滤掉指定范围内的行
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 过滤掉不需要的行
filtered_lines = []
for line in lines:
    if start_keyword in line:
        delete_range = True
        deleted_lines.append(line)  # 将开始关键词行添加到删除行列表
        continue
    if delete_range:
        if end_keyword in line:
            delete_range = False
            filtered_lines.append(line)  # 将结束关键词行添加到输出文件列表
        else:
            deleted_lines.append(line)  # 添加到删除行列表
    else:
        filtered_lines.append(line)
# 将过滤后的内容写入新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)
# 将删除的行写入到新的文件中
with open(deleted_lines_file_path, 'w', encoding='utf-8') as file:
    file.writelines(deleted_lines)
print('过滤完成，结果已保存到:', output_file_path)
print('删除的行已保存到:', deleted_lines_file_path)
###############################################################################################################################################################################
###############################################################################################################################################################################
        
##################################################################################################合并所有频道文件###################################
# 读取要合并的频道文件，并生成临时文件#############################################################合并所有频道文件###################################
file_contents = []
file_paths = ["a0.txt", "港澳.txt", "b.txt", "df0.txt", "f.txt"]  # 替换为实际的文件路径列表#############################################
for file_path in file_paths:                                                             #############################################
    with open(file_path, 'r', encoding="utf-8") as file:                                 #############################################
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("GAT.txt", "w", encoding="utf-8") as output:
    output.write(''.join(file_contents))
           
 ###########################################################################################################################################################################     
# 读取临时文件，并生成结果文件。这一步其实多余，懒得改##############################################################################################################
file_contents = []
file_paths = ["GAT.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
# 写入合并后的文件
with open("综合源.txt", "w", encoding="utf-8") as output:
    output.write(''.join(file_contents))   #加入\n则多一空行
#############################################################去重##################################################################################################################
#############################################################去重#################################################################################################################
with open('综合源.txt', 'r', encoding="utf-8") as file:
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
with open('综合源.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)
#########################################################再次规范频道名######################################################################################################################
#从整理好的文本中进行特定关键词替换以规范频道名#######################################################################################################################################
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
    line = line.replace(" ", "")
    line = line.replace("家庭电影", "家庭影院")    
    line = line.replace("CHC", "")  
    line = line.replace("科技生活", "科技")  
    line = line.replace("财经生活", "财经")  
    line = line.replace("新闻综合", "新闻")  
    line = line.replace("公共新闻", "公共")  
    line = line.replace("经济生活", "经济")  
    line = line.replace("频道1", "频道") 
    line = line.replace("光迅", "酒店")
    line = line.replace("省市频道", "湖北频道")    
    line = line.replace("[720p]", "") 
    line = line.replace("[1080p]", "")     
    print(line, end="")   
##########################################################简体转繁体######################################################################################################################
###############简体转繁体
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
#任务结束，删除不必要的过程文件###########################################################################################################################
files_to_remove = ['湖南电信.txt', '广东电信.txt', '四川电信.txt', '河南电信.txt', '天津联通.txt', '组播源.txt', "GAT.txt", "TW.txt", "a.txt", "a0.txt", "b.txt", "b1.txt", "港澳.txt", "df0.txt", "df.txt", "df1.txt", "sr1.txt", "sr2.txt", \
                   "c2.txt", "c1.txt", "DD.txt", "f.txt", "f1.txt", "ott移动v4.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")
