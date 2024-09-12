
import datetime


# 获取当前日期
current_date = datetime.datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

try:
    # 打开文件并追加日期
    with open('runtime.txt', 'a') as f:
        f.write(f"💚更新时间: {formatted_date},#genre#\nNewTv超级电影,http://39.134.134.47/otttv.bj.chinamobile.com/PLTV/88888888/224/3221226994/1.m3u8?zoneoffset=480&servicetype=1&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%7E%7EV2.0%7EOKgJ-MarN4M0aStGnXjR0A%7EpK8OKM5JoJWWbLRyLfPcUMkwWZ90MzSI9S9PDltJsYzd0ZGcS3Tkh7syciNKJa-w60mDOdwtDyoNwCx9aRgzHNH9AUREV_qvNJtXHRPzYw0%7EExtInfo9bj61dxzlMXrsixrqcFYPg%3D%3D%3A20221022013542%2C915973%2C119.123.71.209%2C20221022013542%2C10000100000000050000000005002658%2C915973%2C-1%2C0%2C1%2C%2C%2C2%2C%2C%2C%2C2%2C%2C371700698%2CEND&GuardEncType=2\n")


except FileNotFoundError:
    print("文件不存在，请检查文件名是否正确。")
