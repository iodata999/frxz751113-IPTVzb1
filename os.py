import os

# 定义要删除的文件列表
files_to_delete = ['酒店源.txt', '组播源.txt']

# 遍历文件列表并删除每个文件
for file in files_to_delete:
    try:
        os.remove(file)
        print(f"成功删除文件： {file}")
    except FileNotFoundError:
        print(f"文件未找到： {file}")
    except Exception as e:
        print(f"删除文件时出错： {file}, 错误信息： {e}")
