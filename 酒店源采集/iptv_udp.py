import os  # 导入os模块，用于操作系统功能，如文件路径和环境变量等
import requests  # 导入requests模块，用于发送HTTP请求
import re  # 导入正则表达式模块，用于字符串匹配和处理
import base64  # 导入base64模块，用于进行base64编码和解码
import cv2  # 导入OpenCV库，用于图像处理（此脚本中未使用）
import datetime  # 注释掉的datetime模块，用于处理日期和时间
from datetime import datetime  # 从datetime模块导入datetime类，用于获取当前时间
from bs4 import BeautifulSoup  # 从bs4模块导入BeautifulSoup类，用于解析HTML和XML文档
from translate import Translator  # 导入Translator类，用于文本翻译
import pytz  # 导入pytz模块，用于处理时区（此脚本中未使用）
from lxml import etree  # 从lxml模块导入etree，用于解析HTML和XML文档
import asyncio  # 导入asyncio模块，用于编写异步代码（此脚本中未使用）
import time  # 导入time模块，用于时间相关功能
#本程序只适用于酒店源的检测，请勿移植他用
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
from queue import Queue
import queue
import replace
import fileinput
from tqdm import tqdm
from pypinyin import lazy_pinyin
from opencc import OpenCC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
header = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
proxy = {
    'http': '139.9.119.20:80',
    'http': '47.106.144.184:7890',
}

# 验证tonkiang可用IP
def via_tonking(url):
    headers = {
        'Referer': 'http://tonkiang.us/hotellist.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    # ip = url
    url = f'http://tonkiang.us/alllist.php?s={url}&c=false&y=false'
    response = requests.get(
        url=url,
        headers=headers,
        verify=False,
        proxies=proxy,
        timeout=10
    )
    # print(response.text)
    et = etree.HTML(response.text)
    div_text = et.xpath('//div[@class="result"]/div/text()')[1]
    if "暂时失效" not in div_text:
        return True
    else:
        return False

# 从tonkiang获取可用IP
def get_tonkiang(key_words):
    result_urls = []
    # urls1 = []
    index = 0
    data = {
        "saerch": f"{key_words}",
        "Submit": " "
    }
    url = "http://tonkiang.us/hoteliptv.php"
    resp = requests.post(url, headers=header, data=data, timeout=10, proxies=proxy)
    resp.encoding = 'utf-8'
    # print(resp.text)
    et = etree.HTML(resp.text)
    divs = et.xpath('//div[@class="tables"]/div')
    for div in divs:
        try:
            status = div.xpath('./div[3]/div/text()')[0]
            if "暂时失效" not in status:
                if index < 1:
                    url = div.xpath('./div[1]/a/b/text()')[0]
                    url = url.strip()
                    if via_tonking(url):
                        result_urls.append(f'http://{url}')
                        index += 1
                else:
                    break
            else:
                continue
        except:
            pass
    return result_urls

# 生成文件
def gen_files(valid_ips, province, isp):
    # 生成节目列表 省份运营商.txt
    index = 0
    print(valid_ips)
    udp_filename = f'rtp/{province}_{isp}.txt'
    with open(udp_filename, 'r', encoding='utf-8') as file:
        data = file.read()
    txt_filename = f'节目表/{province}_{isp}.txt'
    with open(txt_filename, 'w', encoding='utf-8') as new_file:
        new_file.write(f'{province}{isp},#genre#\n')
        for url in valid_ips:
            if index < 3:
                new_data = data.replace("rtp://", f"{url[0]}/udp/")
                new_file.write(new_data)
                new_file.write('\n')
                index += 1
            else:
                continue
    print(f'已生成播放列表，保存至{txt_filename}')

def filter_files(path, ext):
    files = os.listdir(path)
    result = []
    for file in files:
        if file.endswith(ext):
            result.append(file)
    return result

async def via_url(result_url, mcast):
    valid_ips = []
    # 遍历所有视频链接
    # for url in result_urls:
    video_url = result_url + "/udp/" + mcast
    loop = asyncio.get_running_loop()
    future_obj = loop.run_in_executor(None, cv2.VideoCapture, video_url)
    cap = await future_obj
    # 用OpenCV读取视频
    # cap = cv2.VideoCapture(video_url)
    # 检查视频是否成功打开
    if not cap.isOpened():
        print(f"{time.perf_counter()} {video_url} 无效")
    else:
        # 读取视频的宽度和高度
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"{time.perf_counter()} {video_url} 的分辨率为 {width}x{height}")
        # 检查分辨率是否大于0
        if width > 0 and height > 0:
            if len(valid_ips) < 3:
                valid_ips.append(result_url)
            else:
                pass
        # 关闭视频流
        cap.release()
    return valid_ips

# 将任务添加到执行队列中去
async def tasks(url_list, mcast):
    tasks = [via_url(url, mcast) for url in url_list]
    ret = await asyncio.gather(*tasks)
    return ret

# 主入口
def main():
    # 获取udp目录下的文件名
    # files = os.listdir('rtp')
    files = 'rtp'
    files_name = []
    # 去除后缀名并保存至provinces_isps
    for file in filter_files(files, ".txt"):
        name, extension = os.path.splitext(file)
        files_name.append(name)
    # 忽略不符合要求的文件名
    provinces_isps = [name for name in files_name if name.count('_') == 1]
    provinces_isps = sorted(provinces_isps)
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
        # 将省份转成英文小写
        translator = Translator(from_lang='chinese', to_lang='english')
        province_en = translator.translate(province)
        province_en = province_en.lower()
        # 根据不同的 isp 设置不同的 org 值
        org = "Chinanet"
        others = ''
        if isp == "电信" and province_en == "sichuang":
            org = "Chinanet"
            isp_en = "ctcc"
            asn = "4134"
            others = '&& city="Chengdu" '
        elif isp == "电信" and province_en != "sichuang":
            org = "Chinanet"
            isp_en = "ctcc"
            asn = "4134"
        elif isp == "联通" and province_en != "beijing":
            isp_en = "cucc"
            org = "CHINA UNICOM China169 Backbone"
            asn = "4837"
        elif isp == "联通" and province_en == "beijing":
            asn = "4808"
            isp_en = "cucc"
        else:
            asn = ""
            org = ""
        current_time = datetime.now()
        timeout_cnt = 0
        result_urls = set()
        while len(result_urls) == 0 and timeout_cnt <= 5:
            try:
                search_url = 'https://fofa.info/result?qbase64='
                search_txt = f'\"udpxy\" && country=\"CN\" && region=\"{province}\" {others} && asn=\"{asn}\"'
                # 将字符串编码为字节流
                bytes_string = search_txt.encode('utf-8')
                # 使用 base64 进行编码
                search_txt = base64.b64encode(bytes_string).decode('utf-8')
                search_url += search_txt
                print(f"{current_time} 查询运营商 : {province}{isp} ，查询网址 : {search_url}")
                response = requests.get(search_url, headers=header, timeout=30, proxies=proxy)
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
                # urls_all = ['http://106.86.155.109:20005']
                # 去重得到唯一的URL列表
                result_urls = set(urls_all)
                print(f"{current_time} result_urls:{result_urls}")
                valid_ips = asyncio.run(tasks(result_urls, mcast))
                # 异步验证导致返回空值,排除列表空无素
                valid_ips = [e for e in valid_ips if e]
                if valid_ips:
                    gen_files(valid_ips, province, isp)
                else:
                    timeout_cnt += 1
                    print("未找到合适的 IP 地址，重新查询tonking")
                    result_u = get_tonkiang(f'{province}{isp}')
                    if len(result_u) > 0:
                        print(f"{current_time} result_u:{result_u}")
                        valid_ips = asyncio.run(tasks(result_u, mcast))
                        if len(valid_ips) > 0:
                            gen_files(valid_ips, province, isp)
                        else:
                            print("未找到合适的 IP.")
                    else:
                        print("未找到合适的 IP 地址.")
            except (requests.Timeout, requests.RequestException) as e:
                timeout_cnt += 1
                print(f"{current_time} [{province}]搜索请求发生超时，异常次数：{timeout_cnt}")
                if timeout_cnt <= 5:
                    # 继续下一次循环迭代
                    continue
                else:
                    print(f"{current_time} 搜索IPTV频道源[]，超时次数过多：{timeout_cnt} 次，停止处理")
    # 获取节目表目录下的文件名
    # files1 = os.listdir('节目表')
    files1 = '节目表'
    # 过滤TXT文件
    file_contents = []
    for file_path in filter_files(files1, '.txt'):
        with open('节目表/' + file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
        # 移除文件
        # os.remove('节目表/' + file_path)
    # 写入合并后的txt文件
    with open("节目表/IPTV_UDP", "w", encoding="utf-8") as output:
        output.write('\n\n'.join(file_contents))
        # 写入更新日期时间
        # file.write(f"{now_today}更新,#genre#\n")
        # 获取当前时间
        local_tz = pytz.timezone("Asia/Shanghai")
        now = datetime.now(local_tz)
        # now = datetime.now()
        output.write(f"\n更新时间,#genre#\n")
        output.write(f"{now.strftime("%Y-%m-%d")},url\n")
        output.write(f"{now.strftime("%H:%M:%S")},url\n")
    output.close()
    print(f"电视频道成功写入IPTV_UDP")
main()

for line in fileinput.input("节目表/IPTV_UDP", inplace=True):  #打开文件，并对其进行关键词原地替换 
    line = line.replace("CHC电影", "CHC影迷电影") 
    line = line.replace("高清电影", "影迷电影") 
    print(line, end="")  #设置end=""，避免输出多余的换行符   

#从整理好的文本中按类别进行特定关键词提取#
keywords = ['爱动漫', '爱怀旧', '爱经典', '爱科幻', '爱幼教', '爱青春', '爱院线', '爱悬疑']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('节目表/IPTV_UDP', 'r', encoding='utf-8') as file, open('c1.txt', 'w', encoding='utf-8') as c1:    #定义临时文件名
    c1.write('\niHOT系列,#genre#\n')                                                                  #写入临时文件名$GD
    for line in file:
      if '$GD' not in line and '4K' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c1.write(line)  # 将该行写入输出文件                                                          #定义临时文件
 

#从整理好的文本中按类别进行特定关键词提取#
keywords = ['河北', '石家庄', '丰宁', '临漳', '井陉', '井陉矿区', '保定', '元氏', '兴隆', '内丘', '南宫', '吴桥', '唐县', '唐山', '安平', '定州', '大厂', '张家口', '徐水', '成安', \
            '承德', '故城', '康保', '廊坊', '晋州', '景县', '武安', '枣强', '柏乡', '涉县', '涞水', '涞源', '涿州', '深州', '深泽', '清河', '秦皇岛', '衡水', '遵化', '邢台', '邯郸', \
            '邱县', '隆化', '雄县', '阜平', '高碑店', '高邑', '魏县', '黄骅', '饶阳', '赵县', '睛彩河北', '滦南', '玉田', '崇礼', '平泉', '容城', '文安', '三河', '清河']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('节目表/IPTV_UDP', 'r', encoding='utf-8') as file, open('f.txt', 'w', encoding='utf-8') as f:    #定义临时文件名
    f.write('\n河北频道,#genre#\n')                                                                  #写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f.write(line)  # 将该行写入输出文件
            
#从整理好的文本中按类别进行特定关键词提取#
keywords = ['河南', '焦作', '开封', '卢氏', '洛阳', '孟津', '安阳', '宝丰', '邓州', '渑池', '南阳', '内黄', '平顶山', '淇县', '郏县', '封丘', '获嘉', '巩义', '杞县', '汝阳', '三门峡', '卫辉', '淅川', \
            '新密', '新乡', '信阳', '新郑', '延津', '叶县', '义马', '永城', '禹州', '原阳', '镇平', '郑州', '周口']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('节目表/IPTV_UDP', 'r', encoding='utf-8') as file, open('f1.txt', 'w', encoding='utf-8') as f1:    #定义临时文件名
    f1.write('\n河南频道,#genre#\n')                                                                  #写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f1.write(line)  # 将该行写入输出文件

#  获取远程港澳台直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/TW.txt"          #源采集地址
r = requests.get(url)
open('港澳.txt','wb').write(r.content)         #打开源文件并临时写入

#从文本中截取省市段生成两个新文件#
#  获取远程直播源文件，打开文件并输出临时文件并替换关键词
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/汇总.txt"          #源采集地址
r = requests.get(url)
open('TW.txt','wb').write(r.content)         #打开源文件并临时写入
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


#从文本中截取少儿段并生成两个新文件#
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
#
#
        
#合并所有频道文件#
# 读取要合并的频道文件，并生成临时文件#合并所有频道文件#
file_contents = []
file_paths = ["a0.txt", "港澳.txt", "df0.txt", "f.txt", "f1.txt"]  # 替换为实际的文件路径列表#
for file_path in file_paths:                                                             #
    with open(file_path, 'r', encoding="utf-8") as file:                                 #
        content = file.read()
        file_contents.append(content)
# 生成合并后的文件
with open("综合源.txt", "w", encoding="utf-8") as output:
    output.write(''.join(file_contents))   #加入\n则多一空行

#去重#
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
#再次规范频道名#
for line in fileinput.input("综合源.txt", inplace=True):  #打开文件，并对其进行关键词原地替换 
    line = line.replace("4k,", " 4K,") 
    line = line.replace("4K,", " 4K,") 
    line = line.replace("8k,", " 8K,") 
    line = line.replace("8K,", " 8K,") 
    print(line, end="")  #设置end=""，避免输出多余的换行符   
#从整理好的文本中进行特定关键词替换规范频道名#
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
    line = line.replace("CCTV地理世界", "世界地理")  
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
    line = line.replace("省市频道", "湖北频道")    
    line = line.replace("[720p]", "") 
    line = line.replace("[1080p]", "")       
    line = line.replace("[2160p]", "") 
    line = line.replace("[4320p]", "") 
    print(line, end="")   
#简体转繁体#
#简体转繁体
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
#TXT转M3U#
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
#任务结束，删除不必要的过程文件#
files_to_remove = ["TW.txt", "a.txt", "a0.txt", "港澳.txt", "节目表/IPTV_UDP", "df0.txt", "sr1.txt", "c1.txt", \
                   "f.txt", "f1.txt", "节目表/酒店源#.txt"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")
print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")
