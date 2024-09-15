import os
import time


def dynamic_file_naming():
    # 获取当前时间的月日信息
    now = time.localtime()
    month_day = time.strftime('%m%d', now)
    file_extension = '.txt'
    new_file_name = f'file_{month_day}{file_extension}'

    # 假设之前有一个旧的动态命名文件，这里简单查找以'file_'开头的.txt文件作为旧文件
    old_file = None
    for file in os.listdir('.'):
        if file.startswith('file_') and file.endswith('.txt'):
            old_file = file
            break

    if old_file:
        os.rename(old_file, new_file_name)
    else:
        # 如果没有旧文件，则创建新文件
        with open(new_file_name, 'w') as f:
            pass
    return new_file_name


if __name__ == '__main__':
    new_name = dynamic_file_naming()
    print(f'新文件名为: {new_name}')
