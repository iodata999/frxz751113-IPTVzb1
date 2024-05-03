import requests
import re

# 替换为目标IP

ip = '192.168.1.1'

#去重ip
ip_list_all = set()

#设定爬取2次
for _ in range(2):
    url = f'http://tonkiang.us/hoteliptv.php?s={ip}'
    response = requests.get(url)
    ip_list = re.findall(r'href="hoteliptv\.php\?s=([0-9.]+)"', response.text)
    ip_list_all.update(ip_list)

print("获取得到IP：",list(ip_list_all),"\n匹配端口中, 请稍候....") # 输出去重后的ip_list_all列表
#获取酒店源ip_port

with open('ip.txt', 'w') as file:
    for hotel_ip in ip_list_all:
        response = requests.get(f"http://tonkiang.us/hoteliptv.php?s={hotel_ip}")
        if response.status_code == 200:
            ip_ports = re.findall(r"href='hotellist.html\?s=(.*?)'", response.text)
            for ip_port in ip_ports:
                print("获得的IP端口：", ip_port)
                file.write(ip_port + '\n')
                
print("结果已保存到ip.txt")
