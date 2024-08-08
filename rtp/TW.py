import requests
from lxml import etree
import re
import time

url = "http://freegat.us.kg/"

proxy = {
    'http': '223.113.80.158:9091',
}
header = {
    "Referer": "http://twip.xztvtv.site/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=header, proxies=proxy, verify=True)
response.encoding = 'utf-8'
et = etree.HTML(response.text)
print(response.text)
# div[1]/div/div[2]/ul/li[1]
# channels = et.xpath('//div[1]/div/div[2]/ul/li')
# channels = et.xpath('//div[1]/div/div[2]/ul/div[2]/ul/div[2]/ul/div[2]/ul/div[2]/ul/li')
channels = et.xpath('//div[1]/div/div[2]/ul/div[2]/ul/div[2]/ul/div[2]/ul/div[2]/ul/div[2]/ul/li') #推流测试
# channels1 = et.xpath('//div[1]/div/div[2]/ul/li') #特别推荐
# 生成txt文件
txt_content = 'TW,#genre#\n'
with open('TW_PP.txt', 'w', encoding='utf-8') as f:
    f.write(txt_content)
    for channel in channels:
     title = channel.xpath('./div/a/text()')[0]
     title = title[1:]
     # div[1]/div/div[2]/ul/li[1]/div/a/@href
     play_url = channel.xpath('./div/a/@href')[0]
     # print(title, url)
     time.sleep(0.5)
     try:
         play_resp = requests.get(play_url, headers=header, verify=True, timeout=2)
         # print(play_resp.text)
         # p_url = re.findall('videoUrl: "(.*?)";', play_resp.text)[0]         
         p_url = re.findall('videoUrl: "(.*?)",', play_resp.text)[0]
         # print((title + "," + p_url + "\n"))
         f.write(title + "," + p_url + "\n")
     except:
         pass
    # for channel1 in channels1:
    #    title = channel1.xpath('./div/a/text()')[0]
    #    title = title[1:]
    #    # div[1]/div/div[2]/ul/li[1]/div/a/@href
    #    play_url = channel1.xpath('./div/a/@href')[0]
    #    # print(title, url)
    #    time.sleep(0.5)
    #    try:
    #        play_resp = requests.get(play_url, headers=header, verify=True, timeout=2)

    #        p_url = re.findall('videoUrl: "(.*?)",', play_resp.text)[0]
            # print((title + "," + p_url + "\n"))
    #        f.write(title + "," + p_url + "\n")
    #    except:
    #        pass
print("Done!")
