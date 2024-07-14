import os
import requests
import re
import base64
import cv2
# import datetime
from datetime import datetime
from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# pip3 install translate
from translate import Translator
import pytz
from lxml import etree
import asyncio
import time

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
def gen_files(valid_ips, province, isp, province_en, isp_en):
    # 生成节目列表 省份运营商.txt
    index = 0
    print(valid_ips)
    udp_filename = f'files/{province}_{isp}.txt'
    with open(udp_filename, 'r', encoding='utf-8') as file:
        data = file.read()
    txt_filename = f'outfiles/{province_en}_{isp_en}.txt'
    with open(txt_filename, 'w', encoding='utf-8') as new_file:
        new_file.write(f'{province}{isp},#genre#\n')
        for url in valid_ips:
            if index < 3:
                new_data = data.replace("udp://", f"{url[0]}/udp/")
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
    # files = os.listdir('files')
    files = 'files'

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
            with open(f'files/{province_isp}.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines if line.strip()]
            # 获取第一行中以包含 "udp://" 的值作为 mcast
            if lines:
                first_line = lines[0]
                if "udp://" in first_line:
                    mcast = first_line.split("udp://")[1].split(" ")[0]
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
                    gen_files(valid_ips, province, isp, province_en, isp_en)
                else:
                    timeout_cnt += 1
                    print("未找到合适的 IP 地址，重新查询tonking")
                    result_u = get_tonkiang(f'{province}{isp}')
                    if len(result_u) > 0:
                        print(f"{current_time} result_u:{result_u}")
                        valid_ips = asyncio.run(tasks(result_u, mcast))
                        if len(valid_ips) > 0:
                            gen_files(valid_ips, province, isp, province_en, isp_en)
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

    # 获取outfiles目录下的文件名
    # files1 = os.listdir('outfiles')
    files1 = 'outfiles'
    # 过滤TXT文件
    file_contents = []
    for file_path in filter_files(files1, '.txt'):
        with open('outfiles/' + file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)

        # 移除文件
        # os.remove('outfiles/' + file_path)

    # 写入合并后的txt文件
    with open("IPTV_UDP.txt", "w", encoding="utf-8") as output:
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

    print(f"电视频道成功写入IPTV_UDP.txt")


main()
