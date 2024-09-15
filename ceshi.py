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
        try:
            # 如果旧文件存在，先删除旧文件再创建新文件
            os.remove(old_file)
        except OSError as e:
            print(f"删除旧文件 {old_file} 时出错: {e}")
    # 创建新文件
    with open(new_file_name, 'w') as f:
        pass

    # 添加自动更新的重命名（这里简单地在文件名后添加'_updated'）
    new_file_name_updated = new_file_name.rsplit('.', 1)[0]+'_updated.'+new_file_name.rsplit('.', 1)[1]
    os.rename(new_file_name, new_file_name_updated)
    return new_file_name_updated


if __name__ == '__main__':
    new_name = dynamic_file_naming()
    print(f'新文件名为: {new_name}')
