import datetime


def add_run_time_to_m3u(m3u_file_path):
    # 获取当前时间并格式化为字符串
    now = datetime.datetime.now()
    time_str = now.strftime("# Python运行时间: %Y-%m-%d %H:%M:%S\n")
    try:
        with open(m3u_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                lines.insert(1, time_str)
            else:
                lines.append(time_str)
        with open(m3u_file_path, 'w') as f:
            f.writelines(lines)
        print(f"已成功在 {m3u_file_path} 的第二行添加运行时间注释。")
    except FileNotFoundError:
        print(f"文件 {m3u_file_path} 未找到。")


if __name__ == "__main__":
    m3u_file_path = "ceshi.m3u"
    add_run_time_to_m3u(m3u_file_path)
