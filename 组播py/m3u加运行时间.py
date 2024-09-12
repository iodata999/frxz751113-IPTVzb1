import datetime


def add_update_time_to_m3u(iptv_list):
    update_time = datetime.datetime.now().strftime("%Y-%m-%d")
    comment_line = f"# Updated at: {update_time}\n"

    try:
        with open(iptv_list, 'r') as f:
            content = f.read()
            middle_index = len(content) // 2

            new_content = content[:middle_index] + comment_line + content[middle_index:]

        with open(m3u_file_path, 'w') as f:
            f.write(new_content)
        print(f"已成功在 {iptv_list} 中添加更新时间。")
    except FileNotFoundError:
        print(f"文件 {iptv_list} 未找到。")


if __name__ == "__main__":
    m3u_file_path = "iptv_list.m3u"
    add_update_time_to_m3u(iptv_list)
