import datetime


def add_run_time_to_m3u(iptv_list):
    run_time = datetime.datetime.now().strftime("%Y-%m-%d")
    comment_line = f"# Run time: {run_time}\n"

    try:
        with open(iptv_list, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                lines.insert(1, comment_line)
            else:
                lines.append(comment_line)

        with open(iptv_list, 'w') as f:
            f.writelines(lines)
        print(f"已成功在 {iptv_list} 的第二行添加运行时间。")
    except FileNotFoundError:
        print(f"文件 {iptv_list} 未找到。")


if __name__ == "__main__":
    m3u_file_path = "iptv_list.m3u"
    add_run_time_to_m3u(iptv_list.m3u)
