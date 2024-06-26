import re

def remove_duplicates(input_file, output_file):
    url_dict = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            if urls:
                url = urls[0]
                if url not in url_dict:
                    url_dict[url] = line

    with open(output_file, 'w', encoding='utf-8') as f:
        for url, line in url_dict.items():
            f.write(line)

# 使用方法
remove_duplicates('1.txt', 'output.txt')
