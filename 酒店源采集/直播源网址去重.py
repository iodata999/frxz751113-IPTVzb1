import re

def remove_duplicates(input_file, output_file):
    url_dict = {}
    non_url_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        for line in lines:
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            if urls:
                url = urls[0]
                if url not in url_dict:
                    url_dict[url] = line
            else:
                non_url_lines.append(line)

    genre_lines = [line for line in non_url_lines if 'genre' in line.lower()]
    non_genre_lines = [line for line in non_url_lines if 'genre' not in line.lower()]

    with open(output_file, 'w', encoding='utf-8') as f:
        for url, line in url_dict.items():
            f.write(line)
        for line in genre_lines + non_genre_lines:
            f.write(line)

    print("去重后的行数：", len(url_dict) + len(genre_lines) + len(non_genre_lines))

# 使用方法
remove_duplicates('1.txt', 'output.txt')
