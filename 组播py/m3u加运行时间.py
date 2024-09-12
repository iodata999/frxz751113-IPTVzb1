import datetime


def add_run_time_to_m3u(m3u_file_path):
    # 获取当前日期和时间并格式化为字符串
    run_time = datetime.datetime.now().strftime("%Y-%m - d %H:%M:%S")
    comment_line = f"# Python运行时间: {run_time}\n"

    try:
        with open(m3u_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                lines.insert(1, comment_line)
            else:
                lines.append(comment_line)

        with open(m3u_file_path, 'w') as f:
            f.writelines(lines)
        print(f"已成功在 {m3u_file_path} 的第二行添加运行时间注释。")
    except FileNotFoundError:
        print(f"文件 {m3u_file_path} 未找到。")


if __name__ == "__main__":
    m3u_file_path = "ceshi.m3u"
    add_run_time_to_m3u(m3u_file_path)
