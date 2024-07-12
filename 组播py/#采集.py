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








# 合并自定义频道文件#################################################################################################
file_contents = []
file_paths = ["四川电信.txt", "广东电信.txt", "天津联通.txt", "江苏电信.txt", "湖北电信.txt", "湖南电信.txt", "河北电信.txt", "安徽电信.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("合并.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    


#替换多余的关键字词###################################################################################################
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



#二次替换某些关键词为便于排序的自定义词####################################################################################################
for line in fileinput.input("合并.txt", inplace=True):  #打开文件，并对其进行原地替换
    
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


#对替换完成的文本进行排序#####################################################################################################################

with open('合并.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines.sort()

with open('排序.txt', 'w', encoding='UTF-8') as f:
    for line in lines:
        f.write(line)


#再次替换自定义词为常规词##########################################################################################################################
for line in fileinput.input("排序.txt", inplace=True):  #打开文件，并对其进行原地替换
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
keywords = ['CCTV1,', 'CCTV10,', 'CCTV11,', 'CCTV12,', 'CCTV13,', 'CCTV14,', 'CCTV15,', 'CCTV16,', 'CCTV164k,', 'CCTV17,', 'CCTV2,', 'CCTV3,', 'CCTV4,', 'CCTV5,', 'CCTV5+,', 'CCTV6,', 'CCTV7,', 'CCTV8,', 'CCTV9,', '环绕']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('央视频道,#genre#\n')                                                                  #####写入临时文件名
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
keywords = ['风云', '兵器', '女性', '地理', '央视文化', '风云', '怀旧剧场', '第一剧场', 'CHC']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('e.txt', 'w', encoding='utf-8') as e:    #####定义临时文件名
    e.write('\n央视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
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




##########################################################################################################################################################################################
keywords = ['卫视', '凤凰']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('ws.txt', 'w', encoding='utf-8') as ws:
    ws.write('\n卫视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          ws.write(line)  # 将该行写入输出文件


###############################################################################################################################################################################
keywords = ['4K', '8K']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('DD.txt', 'w', encoding='utf-8') as DD:
    DD.write('\n4K 频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          DD.write(line)  # 将该行写入输出文件

for line in fileinput.input("DD.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      


###############################################################################################################################################################################            
keywords = ['热门剧场', '经典剧场', '抗战剧场', '谍战剧场', '军旅剧场', '华语影院', '影', '剧', '淘', '爱']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('ys.txt', 'w', encoding='utf-8') as ys:
    ys.write('\n影视频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          ys.write(line)  # 将该行写入输出文件

for line in fileinput.input("ys.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      



###############################################################################################################################################################################
keywords = ['湖南', '广东', '武汉', '湖北', '安徽', '天津', '河北', '石家庄', '珠海', '广州']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('df.txt', 'w', encoding='utf-8') as df:
    df.write('\n省市频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          df.write(line)  # 将该行写入输出文件
for line in fileinput.input("df.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      

###############################################################################################################################################################################
keywords = ['综合', '公共', '生活', '新闻', '电视', '科技', '文艺', '经济']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('xs.txt', 'w', encoding='utf-8') as xs:
    xs.write('\n地方频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          xs.write(line)  # 将该行写入输出文件
for line in fileinput.input("xs.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      


###############################################################################################################################################################################
keywords = [',']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('排序.txt', 'r', encoding='utf-8') as file, open('qt.txt', 'w', encoding='utf-8') as qt:
    qt.write('\n其他频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          qt.write(line)  # 将该行写入输出文件
for line in fileinput.input("qt.txt", inplace=True):  #打开文件，并对其进行关键词原地替换                     ###########
    line = line.replace("AA", "")                                                                         ###########                                                      ###########
    print(line, end="")  #设置end=""，避免输出多余的换行符      






# 读取要合并的频道文件，并生成临时文件##############################################################################################################
file_contents = []
file_paths = ["c.txt", "e.txt", "ws.txt", "DD.txt", "ys.txt", "df.txt", "xs.txt", "qt.txt"]  # 替换为实际的文件路径列表
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
with open("组播合并.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

for line in fileinput.input("组播合并.txt", inplace=True):  #打开文件，并对其进行关键词原地替换  
    line = line.replace("固定源", "固定")   
    line = line.replace("更新", "")             
    line = line.replace("港澳频道/", "港澳/")    
    print(line, end="")  #设置end=""，避免输出多余的换行符   

#########原始顺序去重，以避免同一个频道出现在不同的类中
with open('组播合并.txt', 'r', encoding="utf-8") as file:
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
with open('组播合并.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)
#####################






###########################################################################################################################################################################
#任务结束，删除不必要的过程文件###########################################################################################################################

os.remove("GAT.txt")
os.remove("ws.txt")
os.remove("DD.txt")
os.remove("df.txt")
os.remove("ys.txt")
os.remove("xs.txt")
os.remove("qt.txt")
os.remove("c.txt")
os.remove("e.txt")


file_paths = ["四川电信.txt", "广东电信.txt", "天津联通.txt", "江苏电信.txt", "湖北电信.txt", "湖南电信.txt", "河北电信.txt", "安徽电信.txt"] 
for file_path in file_paths:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"文件 {file_path} 已成功删除")
    else:
        print(f"文件 {file_path} 不存在")
print("任务运行完毕，分类频道列表可查看文件夹内结果.txt文件！")
