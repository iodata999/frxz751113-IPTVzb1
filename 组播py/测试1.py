import os
import glob

def merge_files(folder_path, output_file):
    # 获取文件夹中的所有文件
    files = glob.glob(os.path.join(folder_path, '*'))

    # 创建一个新的文件用于合并
    with open(output_file, 'w') as outfile:
        # 遍历文件夹中的每个文件
        for file in files:
            # 打开文件并读取内容
            with open(file, 'r') as infile:
                # 将文件内容写入到新的文件中
                outfile.write(infile.read())
                # 添加换行符以分隔不同文件的内容
                outfile.write('')

# 使用示例
folder_path = 'outfiles'  # 替换为你的文件夹路径
output_file = '测试.txt'  # 替换为你想要保存合并后的文件名
merge_files(folder_path, output_file)
