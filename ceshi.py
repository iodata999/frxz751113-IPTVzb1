import os
import time


def dynamic_file_naming():
    # 获取当前时间的月日信息
    now = time.localtime()
    month_day = time.strftime('%m%d', now)
    file_extension = '.txt'
    new_file_name = f'file_{month_day}{file_extension}'

    # 查找旧文件
    old_file = None
    for file in os.listdir('.'):
        if file.startswith('file_') and file.endswith('.txt'):
            old_file = file
            break

    if old_file:
        # 如果旧文件存在，读取旧文件内容，先删除旧文件再创建新文件并写入旧内容
        with open(old_file, 'r') as f:
            content = f.read()
        os.remove(old_file)
        with open(new_file_name, 'w') as f:
            f.write(content)
    else:
        # 创建新文件
        with open(new_file_name, 'w') as f:
            pass

    return new_file_name


if __name__ == '__main__':
    new_name = dynamic_file_naming()
    print(f'新文件名为: {new_name}')
    
