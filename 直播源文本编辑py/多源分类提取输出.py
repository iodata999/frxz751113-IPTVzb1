import os

def extract_keywords(file_path, keywords):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line for line in lines if any(keyword in line for keyword in keywords)]

def write_to_file(output_file, lines, keywords):
    with open(output_file, 'w', encoding='utf-8') as file:
        # 在第一行写入提取的关键词
        file.write("央视频道,#genre#\n")
        # 接着写入其他行
        file.writelines(lines)

def main():
    keyword_files = ['file1.txt', 'file2.txt', 'file3.txt']  # 替换为你需要处理的文件名列表
    keywords = ['CCTV']  # 替换为你需要查找的关键字列表,可以多个关键词用,隔开
    output_file = 'output.txt'  # 输出文件名

    all_lines = {}
    for keyword in keywords:
        all_lines[keyword] = []

    for file_path in keyword_files:
        if os.path.exists(file_path):
            lines = extract_keywords(file_path, keywords)
            for line in lines:
                for keyword in keywords:
                    if keyword in line:
                        all_lines[keyword].append(line)
        else:
            print(f"文件 {file_path} 不存在")

    for keyword, lines in all_lines.items():
        output_file_for_keyword = f"{keyword}_output.txt"
        write_to_file(output_file_for_keyword, lines, keywords)
        print(f"已将包含关键字 {keyword} 的行写入 {output_file_for_keyword}")

if __name__ == '__main__':
    main()
