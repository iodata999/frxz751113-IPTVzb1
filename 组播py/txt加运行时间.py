
import datetime


def add_run_date_to_txt(txt_file_path):
    # 获取当前日期
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%Y-%m-%d")

    try:
        with open(txt_file_path, 'r') as f:
            content = f.read()
        new_content = date_str + '\n' + content

        with open(txt_file_path, 'w') as f:
            f.write(new_content)
        print(f"已成功在 {txt_file_path} 的第一行添加运行日期。")
    except FileNotFoundError:
        print(f"文件 {txt_file_path} 未找到。")


if __name__ == "__main__":
    txt_file_path = "runtime.txt"
    add_run_date_to_txt(txt_file_path)

    
      #  f.write(f"💚更新时间: {formatted_date},#genre#\nNewTv超级电影,http://39.134.134.47/otttv.bj.chinamobile.com/PLTV/88888888/224/3221226994/1.m3u8?zoneoffset=480&servicetype=1&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%7E%7EV2.0%7EOKgJ-MarN4M0aStGnXjR0A%7EpK8OKM5JoJWWbLRyLfPcUMkwWZ90MzSI9S9PDltJsYzd0ZGcS3Tkh7syciNKJa-w60mDOdwtDyoNwCx9aRgzHNH9AUREV_qvNJtXHRPzYw0%7EExtInfo9bj61dxzlMXrsixrqcFYPg%3D%3D%3A20221022013542%2C915973%2C119.123.71.209%2C20221022013542%2C10000100000000050000000005002658%2C915973%2C-1%2C0%2C1%2C%2C%2C2%2C%2C%2C%2C2%2C%2C371700698%2CEND&GuardEncType=2\n")
