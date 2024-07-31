from pypinyin import lazy_pinyin
import re
import os
#a = input('FileName(DragHere):')
#with open(a, 'r', encoding="utf-8") as f:#拖入文件操作

# 打开一个utf-8编码的文本文件
with open("iptv_list.txt", "r", encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序，按照第一个数字的大小排列，其余行按中文排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))

# 将排序后的行写入新的utf-8编码的文本文件
with open("2.txt", "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)





###############################        
with open('2.txt', 'r', encoding='utf-8') as file:
#从整理好的文本中按类别进行特定关键词提取#############################################################################################
 keywords = ['CCTV', '4K']  # 需要提取的关键字列表
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:    #####定义临时文件名
    a.write('\n央视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line and '环绕' not in line and '风' not in line and '兵' not in line and '女' not in line and '文' not in line\
         and '影' not in line and '剧' not in line and '地' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         a.write(line)  # 将该行写入输出文件 


###############################        
with open('2.txt', 'r', encoding='utf-8') as file:
#从整理好的文本中按类别进行特定关键词提取#############################################################################################
 keywords = ['环绕', '风云', '兵器', '女性', '地理', '央视文化', '风云', '怀旧剧场', '第一剧场', 'CHC']  # 需要提取的关键字列表
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('a1.txt', 'w', encoding='utf-8') as a1:    #####定义临时文件名
    for line in file:
      if 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         a1.write(line)  # 将该行写入输出文件 




################
keywords = ['卫视', '星空', '凤凰']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:    #####定义临时文件名
    b.write('\n卫视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line:        
        if re.search(pattern, line):  # 如果行中有任意关键字
         b.write(line)  # 将该行写入输出文件

         
################
keywords = ['爱情', '超级电', '妈', '功夫', '古装', '东北', '黑莓', '欢乐', '动作电影', '大剧', '家庭', '军旅', 'New', '影', '大片', '惊', '院线', '精', '重温', '剧']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n影视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
       if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and '江苏' not in line and '浙江' not in line and '安徽' not in line and '上虞' not in line and '黑龙江' not in line and '四川' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件



        
################
keywords = ['河北', '石家庄', '丰宁', '临漳', '井陉', '井陉矿区', '保定', '元氏', '兴隆', '内丘', '南宫', '吴桥', '唐县', '唐山', '安平', '定州', '大厂', '张家口', '徐水', '成安', \
            '承德', '故城', '康保', '廊坊', '晋州', '景县', '武安', '枣强', '柏乡', '涉县', '涞水', '涞源', '涿州', '深州', '深泽', '清河', '秦皇岛', '衡水', '遵化', '邢台', '邯郸', \
            '邱县', '隆化', '雄县', '阜平', '高碑店', '高邑', '魏县', '黄骅', '饶阳', '赵县', '睛彩河北', '滦南', '玉田', '崇礼', '平泉', '容城', '文安', '三河', '清河']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f.txt', 'w', encoding='utf-8') as f:    #####定义临时文件名
    f.write('\n河北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f.write(line)  # 将该行写入输出文件


###############f1
keywords = ['河南', '焦作', '开封', '卢氏', '洛阳', '孟津', '安阳', '宝丰', '邓州', '渑池', '南阳', '内黄', '平顶山', '淇县', '郏县', '封丘', '获嘉', '巩义', '杞县', '汝阳', '三门峡', '卫辉', '淅川', \
            '新密', '新乡', '信阳', '新郑', '延津', '叶县', '义马', '永城', '禹州', '原阳', '镇平', '郑州', '周口']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f1.txt', 'w', encoding='utf-8') as f1:    #####定义临时文件名
    f1.write('\n河南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f1.write(line)  # 将该行写入输出文件



################
keywords = ['湖南', '长沙', '常德', '郴州', '茶', '金鹰', '钓', '衡阳', '怀化', '吉首', '娄底', '邵阳', '湘潭', '益阳', '永州', '岳阳', '张家界', '株洲']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('h1.txt', 'w', encoding='utf-8') as h1:    #####定义临时文件名
    h1.write('\n湖南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         h1.write(line)  # 将该行写入输出文件



################
keywords = ['广东', '潮州', '东莞', '佛山', '广州', '河源', '惠州', '江门', '揭阳', '茂名', '梅州', '清远', '汕头', '汕尾', '韶关', '深圳', '阳江', '云浮', '湛江', \
            '肇庆', '中山', '珠海']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('k.txt', 'w', encoding='utf-8') as k:    #####定义临时文件名
    k.write('\n广东频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         k.write(line)  # 将该行写入输出文件



################
keywords = ['四川', '阿坝', '巴中', '成都', '达州', '德阳', '甘孜', '广安', '广元', '乐山', '凉山', '乐山', '大片', '爱', '眉山', '绵阳', '内江', '南充', '攀枝花', '遂宁', '雅安', \
            '宜宾', '资阳', '自贡', '上海', '东方', '财经', '五星']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('n.txt', 'w', encoding='utf-8') as n:    #####定义临时文件名
    n.write('\n四川上海,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         n.write(line)  # 将该行写入输出文件



################
keywords = [',']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('l.txt', 'w', encoding='utf-8') as l:    #####定义临时文件名
    l.write('\n其他频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         l.write(line)  # 将该行写入输出文件

         

############
file_contents = []
file_paths = ["a.txt", "a1.txt", "b.txt", "c.txt", "f.txt", "f1.txt", "k.txt", "h1.txt",  \
              "n.txt",  "l.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("去重.txt", "w", encoding="utf-8") as output:
    output.write(''.join(file_contents))

##############################原始顺序去重
# 打开文档并读取所有行 
with open('去重.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
 
# 使用列表来存储唯一的行的顺序 
 unique_lines = [] 
 seen_lines = set() 

# 遍历每一行，如果是新的就加入unique_lines 
for line in lines:
 if line not in seen_lines:
  unique_lines.append(line)
  seen_lines.add(line)

# 将唯一的行写入新的文档 
with open('iptv_list.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)
##############################






files_to_remove = ["a.txt", "a1.txt", "a2.txt", "b.txt", "c.txt", "2.txt", "f.txt", "f1.txt", "h1.txt", "k.txt", "n.txt", "l.txt", "去重.txt"]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")


print("任务运行完毕")






