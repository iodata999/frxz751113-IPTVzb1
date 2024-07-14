# 合并自定义频道文件#################################################################################################
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
file_contents = []
file_paths = ["四川电信.txt", "广东电信.txt", "天津联通.txt", "湖南电信.txt", "河南电信.txt", "河北电信.txt"]  # 替换为实际的文件路径列表
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
    print(line, end="")  #设置end=""，避免输出多余的换行符   








#从整理好的文本中按类别进行特定关键词提取#############################################################################################
keywords = ['环绕', '爱动漫', '爱怀旧', '爱经典', '爱科幻', '爱幼教', '爱青春', '爱悬疑']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n高质组播,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件                                                          #####定义临时文件
 








##########################################################################E#####################################################################################
keywords = ['风云', '兵器', '女性', '地理', '央视文化', '风云', '剧', '影', 'CHC', '星空', '凤凰']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('e.txt', 'w', encoding='utf-8') as e:    #####定义临时文件名
    for line in file:
      if '环绕' not in line and 'CCTV' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         e.write(line)  # 将该行写入输出文件                                                          #####定义临时文件






###############################################################################################################################################################################
keywords = ['4K', '8K']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('DD.txt', 'w', encoding='utf-8') as DD:
    DD.write('\n4K 频道,#genre#\n')
    for line in file:
      if '环绕' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
          DD.write(line)  # 将该行写入输出文件



###############################################################################################################################################################################
keywords = ['湖南', '广东', '天津', '广州', '河北']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('df.txt', 'w', encoding='utf-8') as df:
    df.write('\n省市频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line and '4K' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          df.write(line)  # 将该行写入输出文件





###############################################################################################################################################################################
keywords = ['综合', '公共', '生活', '新闻', '电视', '文艺', '佛山', '深圳', '珠海', '石家庄', '经济']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('组播源.txt', 'r', encoding='utf-8') as file, open('xs.txt', 'w', encoding='utf-8') as xs:
    xs.write('\n地方频道,#genre#\n')
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and '影' not in line and '剧' not in line and '湖南' not in line and '广东' not in line and '湖北' not in line and '安徽' not in line and '天津' not in line and '河北' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
          xs.write(line)  # 将该行写入输出文件





######################################################################################################################打开欲要最终合并的文件并输出临时文件并替换关键词
with open('酒店源.txt', 'r', encoding='utf-8') as f:  #打开文件，并对其进行关键词提取                                               ###########
 #keywords = ['http', 'rtmp', 'genre']  # 需要提取的关键字列表                                                       ###########
 keywords = ['重温', '酒店', '私人', '天映', '莲花', 'AXN', '好莱坞', '星', '龙祥', '凤凰', '东森']  # 需要提取的关键字列表                                                       ###########
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字                                      ###########
 #pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制                                                     ###########
 with open('酒店源.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:           ###########
    b.write('\n港澳频道,#genre#\n')                                                                        ###########
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
    


##############################################################################################################################################################################################################################################

#  获取远程港澳台直播源文件，打开文件并输出临时文件并替换关键词
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/TW.txt"          #源采集地址
r = requests.get(url)
open('TW.txt','wb').write(r.content)         #打开源文件并临时写入
#keywords = ['http', 'rtmp']  # 需要提取的关键字列表 8M1080
#pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
pattern = r"^(.*?),(?!#genre#)(.*?)$" #直接复制不带分类行
with open('TW.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          a.write(line)  # 将该行写入输出文件
for line in fileinput.input("a.txt", inplace=True):   #打开临时文件原地替换关键字
    line = line.replace("﻿Taiwan,#genre#", "")                         #编辑替换字
    line = line.replace("﻿amc", "AMC")                         #编辑替换字
    line = line.replace("﻿中文台", "中文")                         #编辑替换字
    print(line, end="")                                     #加入此行去掉多余的转行符


#  获取远程直播源文件
url = "https://raw.githubusercontent.com/frxz751113/AAAAA/main/IPTV/ott%E7%A7%BB%E5%8A%A8V6%E5%9B%9E%E6%94%BE.txt"          #源采集地址
r = requests.get(url)
open('ott移动v4.txt','wb').write(r.content)         #打开源文件并临时写入

keywords = ['']  # 需要提取的关键字列表，留空则全局选择
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #去掉genre行直接复制
with open('ott移动v4.txt', 'r', encoding='utf-8') as file, open('TT.txt', 'w', encoding='utf-8') as TT:
    #TT.write('\n央视频道,#genre#\n')
    for line in file:
        if re.search(pattern, line):  # 如果行中有任意关键字
          TT.write(line)  # 将该行写入输出文件
        


###########################################################################################################################################################################
# 读取要合并的频道文件，并生成临时文件##############################################################################################################
file_contents = []
file_paths = ["TT.txt", "b.txt", "a.txt", "c.txt", "e.txt", "DD.txt", "df.txt", "xs.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
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
###########################################################################################################################################################################
# 写入合并后的文件
with open("综合源.txt", "w", encoding="utf-8") as output:
    output.write(''.join(file_contents))

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




###########################################################################################################################################################################
#任务结束，删除不必要的过程文件###########################################################################################################################
os.remove("GAT.txt")
os.remove("DD.txt")
os.remove("TW.txt")
os.remove("a.txt")
os.remove("b.txt")
os.remove("c.txt")
os.remove("e.txt")
os.remove("xs.txt")
os.remove("df.txt")
os.remove("TT.txt")
os.remove("ott移动v4.txt")



files_to_remove = ['湖南电信.txt', '四川电信.txt', '广东电信.txt', '天津联通.txt', '河北电信.txt', '湖南电信.m3u', '河南电信.m3u', '河南电信.txt', '四川电信.m3u', '广东电信.m3u', '天津联通.m3u', '河北电信.m3u']

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")

print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")
