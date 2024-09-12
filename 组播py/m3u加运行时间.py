def txt_to_m3u(txt_file_path, m3u_file_path):
    try:
        with open(txt_file_path, 'r') as txt_f:
            lines = txt_f.readlines()
            with open(m3u_file_path, 'w') as m3u_f:
                m3u_f.write('#EXTM3U\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        m3u_f.write(f'#EXTINF:-1,\n{line}\n')
        print(f"已成功将 {txt_file_path} 转换为 {m3u_file_path}")
    except FileNotFoundError:
        print(f"文件 {txt_file_path} 或 {m3u_file_path} 未找到。")


if __name__ == "__main__":
    txt_file_path = "ceshi.txt"
    m3u_file_path = "ceshi.m3u"
    txt_to_m3u(txt_file_path, m3u_file_path)
