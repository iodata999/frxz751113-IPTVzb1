def merge_txt_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_path, 'w') as output_file:
        content1 = file1.read()
        content2 = file2.read()
        output_file.write(content1 + content2)

# 请替换为您实际的文件路径
file1_path = 'iptv_list.txt'  
file2_path = 'yeye.txt'  
output_path = 'merged.txt'  

merge_txt_files(file1_path, file2_path, output_path)
