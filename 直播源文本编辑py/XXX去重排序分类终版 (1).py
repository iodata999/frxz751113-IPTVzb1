from pypinyin import lazy_pinyin
import re
import os
#a = input('FileName(DragHere):')
#with open(a, 'r', encoding="utf-8") as f:#拖入文件操作

# 打开一个utf-8编码的文本文件
with open("1.txt", "r", encoding="utf-8") as file:
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
 keywords = ['CCTV', '风云音乐', '女性', '地理', '风云剧场', '怀旧剧场', '第一剧场', '家庭', '影迷', '高清电影', '动作电影', 'CHC', '世界地理', '兵器', \
             '央视台球', '第一剧场', '风云足球', '高尔夫', '动作电影', '家庭影院', '影迷电影', '世界地理']  # 需要提取的关键字列表
 pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('a.txt', 'w', encoding='utf-8') as a:    #####定义临时文件名
    a.write('\n央视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         a.write(line)  # 将该行写入输出文件 

################
keywords = ['卫视', '星空', '凤凰']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('b.txt', 'w', encoding='utf-8') as b:    #####定义临时文件名
    b.write('\n卫视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'genre' not in line and 'epg' not in line:       
        if re.search(pattern, line):  # 如果行中有任意关键字
         b.write(line)  # 将该行写入输出文件

         
################
keywords = ['爱情', '重温经典', '军事评论', '农业致富', '哒啵赛事', '怡伴健康', '明星大片', '武博世界', '中国功夫', '军旅', '炫舞未来', '精品体育', '精品萌宠', '精品记录', '超级体育', '超级', '金牌', \
            '东北热剧', '中国功夫', '军旅剧场', '古装剧场', '家庭剧场', '惊悚悬疑', '欢乐剧场', '潮妈辣婆', '爱情喜剧', '精品大剧', '超级影视', '超级电影', '黑莓动画', '黑莓电影', \
            '海外剧场', '精彩影视', '七彩戏剧', '东方影视', '无名影视', '潮婆辣妈', '超级剧', '热播精选', '武术世界', '求索动物', '求索', '求索科学', '求索记录', '精品纪录']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('c.txt', 'w', encoding='utf-8') as c:    #####定义临时文件名
    c.write('\n影视频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
       if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'epg' not in line and '江苏' not in line and '浙江' not in line and '安徽' not in line and '上虞' not in line and '黑龙江' not in line and '四川' not in line and 'genre' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         c.write(line)  # 将该行写入输出文件

############
keywords = ['TVB', '三立', '八大', '中天', '中视', '东森', '凤凰', '天映', '美亚', '环球', '翡翠', '亚洲', '大爱', '大愛', \
            '明珠', '半岛', 'AMC', '龙祥', '台视', '1905', '纬来', '神话', '经典都市', '视界', '番薯', '私人', '酒店', 'TVB', '凤凰', '半岛', '星光视界', '番薯', '大愛', '新加坡', '星河', '明珠', '环球', '翡翠台']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
with open('2.txt', 'r', encoding='utf-8') as file, open('d.txt', 'w', encoding='utf-8') as d:    #####定义临时文件名
    d.write('\n港澳频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
        if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and '江苏' not in line and '浙江' not in line and '四川' not in line and 'genre' not in line and 'epg' not in line:
          if re.search(pattern, line): 
              d.write(line)  # 将该行写入输出文件

################
keywords = ['江苏', '常州', '淮安', '连云港', '南京', '南通', '高邮', '苏州', '宿迁', '泰州', '无锡', '徐州', '盐城', '扬州', '镇江']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('e.txt', 'w', encoding='utf-8') as e:    #####定义临时文件名
    e.write('\n江苏频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:   
        if re.search(pattern, line):  # 如果行中有任意关键字
         e.write(line)  # 将该行写入输出文件

################
keywords = ['江西', '抚州', '赣州', '吉安', '景德镇', '九江', '南昌', '萍乡', '上饶', '新余', '宜春', '鹰潭']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('e1.txt', 'w', encoding='utf-8') as e1:    #####定义临时文件名
    e1.write('\n江西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:   
        if re.search(pattern, line):  # 如果行中有任意关键字
         e1.write(line)  # 将该行写入输出文件

         
################
keywords = ['河北', '石家庄', '丰宁', '临漳', '井陉', '井陉矿区', '保定', '元氏', '兴隆', '内丘', '南宫', '吴桥', '唐县', '唐山', '安平', '定州', '大厂', '张家口', '徐水', '成安', \
            '承德', '故城', '康保', '廊坊', '晋州', '景县', '武安', '枣强', '柏乡', '涉县', '涞水', '涞源', '涿州', '深州', '深泽', '清河', '秦皇岛', '衡水', '遵化', '邢台', '邯郸', \
            '邱县', '隆化', '雄县', '阜平', '高碑店', '高邑', '魏县', '黄骅', '饶阳', '赵县', '睛彩河北', '滦南', '玉田', '崇礼', '平泉', '容城', '文安', '三河', '清河']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f.txt', 'w', encoding='utf-8') as f:    #####定义临时文件名
    f.write('\n河北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f.write(line)  # 将该行写入输出文件




################f1
keywords = ['河南', '焦作', '开封', '卢氏', '洛阳', '孟津', '渑池', '南阳', '内黄', '平顶山', '淇县', '杞县', '汝阳', '三门峡', '卫辉', '淅川', \
            '新密', '新乡', '信阳', '新郑', '延津', '叶县', '义马', '永城', '禹州', '原阳', '镇平', '郑州', '周口']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('f1.txt', 'w', encoding='utf-8') as f1:    #####定义临时文件名
    f1.write('\n河南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         f1.write(line)  # 将该行写入输出文件




         
################
keywords = ['浙江', '杭州', '宁波', '丽水', '上虞', '绍兴', '温州', '永嘉', '诸暨', '钱江', '松阳', '苍南', '遂昌', '青田', '龙泉', '余杭', '新昌', '杭州', '余杭', '丽水', '龙泉', \
            '青田', '松阳', '遂昌', '宁波', '余姚', '上虞', '新商都', '绍兴', '温州', '永嘉', '诸暨', '钱江', '国际', '苍南']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('g.txt', 'w', encoding='utf-8') as g:    #####定义临时文件名
    g.write('\n浙江频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         g.write(line)  # 将该行写入输出文件



################
keywords = ['湖北', '武汉', '松滋', '十堰', '咸宁', '远安', '黄石', '荆州', '当阳', '恩施', '五峰', '来凤', '枝江', '黄冈', '随州', '荆门', '秭归', '孝感', \
            '鄂州', '湖北', '五峰', '来凤', '枝江', '随州', '荆门', '秭归', '孝感', '鄂州', '武汉', '松滋', '十堰', '咸宁', '黄石', '垄上', '荆州', '当阳', '恩施', '宜都']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('h.txt', 'w', encoding='utf-8') as h:    #####定义临时文件名
    h.write('\n湖北频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         h.write(line)  # 将该行写入输出文件




################
keywords = ['湖南', '长沙', '常德', '郴州', '衡阳', '怀化', '吉首', '娄底', '邵阳', '湘潭', '益阳', '永州', '岳阳', '张家界', '株洲']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('h1.txt', 'w', encoding='utf-8') as h1:    #####定义临时文件名
    h1.write('\n湖南频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         h1.write(line)  # 将该行写入输出文件







################
keywords = ['陕西', '安康', '宝鸡', '汉中', '商洛', '铜川', '渭南', '西安', '咸阳', '延安', '榆林']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('i.txt', 'w', encoding='utf-8') as i:    #####定义临时文件名
    i.write('\n陕西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         i.write(line)  # 将该行写入输出文件








################
keywords = ['黑龙江', '大庆', '大兴安岭', '哈尔滨', '鹤岗', '黑河', '鸡西', '佳木斯', '牡丹江', '七台河', '齐齐哈尔', '双鸭山', '绥化', '伊春']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('j.txt', 'w', encoding='utf-8') as j:    #####定义临时文件名
    j.write('\n黑龙江频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         j.write(line)  # 将该行写入输出文件











################
keywords = ['广东', '潮州', '东莞', '佛山', '广州', '河源', '惠州', '江门', '揭阳', '茂名', '梅州', '清远', '汕头', '汕尾', '韶关', '深圳', '阳江', '云浮', '湛江', \
            '肇庆', '中山', '珠海']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('k.txt', 'w', encoding='utf-8') as k:    #####定义临时文件名
    k.write('\n广东频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         k.write(line)  # 将该行写入输出文件









################
keywords = ['广西', '百色', '北海', '防城港', '桂林', '河池', '柳州', '南宁', '钦州', '梧州', '玉林']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('k1.txt', 'w', encoding='utf-8') as k1:    #####定义临时文件名
    k1.write('\n广西频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         k1.write(line)  # 将该行写入输出文件











################
keywords = ['云南', '版纳', '保山', '楚雄', '大理', '德宏', '迪庆', '红河', '昆明', '丽江', '临沧', '怒江', '曲靖', '思茅', '文山', '玉溪', '昭通', '西双版纳', '贵州', \
            '安顺', '毕节', '都匀', '贵阳', '凯里', '六盘水', '铜仁', '兴义', '遵义']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('m.txt', 'w', encoding='utf-8') as m:    #####定义临时文件名
    m.write('\n云贵频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         m.write(line)  # 将该行写入输出文件


################
keywords = ['四川', '阿坝', '巴中', '成都', '达州', '德阳', '甘孜', '广安', '广元', '乐山', '凉山', '泸州', '眉山', '绵阳', '内江', '南充', '攀枝花', '遂宁', '雅安', \
            '宜宾', '资阳', '自贡', '上海', '东方', '财经', '五星', '四川', '黑水', '金川', '乐至', '双流', '万源', '马尔康', '泸县', '文山', '什邡', '西青', '长宁', '达州', '红河']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('n.txt', 'w', encoding='utf-8') as n:    #####定义临时文件名
    n.write('\n四川上海,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         n.write(line)  # 将该行写入输出文件



################
keywords = ['安徽', '安庆', '蚌埠', '亳州', '巢湖', '池州', '滁州', '阜阳', '合肥', '淮北', '淮南', '黄山', '六安', '马鞍山', '宿州', '铜陵', '芜湖', '宣城', '山东', '滨州', \
            '德州', '东营', '菏泽', '济南', '济宁', '莱芜', '聊城', '临沂', '青岛', '日照', '泰安', '威海', '潍坊', '烟台', '枣庄', '淄博', '山西', '长治', '大同', '晋城', \
            '晋中', '临汾', '吕梁', '朔州', '太原', '忻州', '阳泉', '运城']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('o.txt', 'w', encoding='utf-8') as o:    #####定义临时文件名
    o.write('\n安徽山西,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         o.write(line)  # 将该行写入输出文件
                  
################         
                  
################
keywords = [',']  # 需要提取的关键字列表
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('2.txt', 'r', encoding='utf-8') as file, open('l.txt', 'w', encoding='utf-8') as l:    #####定义临时文件名
    l.write('\n其他频道,#genre#\n')                                                                  #####写入临时文件名
    for line in file:
      if 'CCTV' not in line and '卫视' not in line and 'CHC' not in line and '4K' not in line and 'genre' not in line and 'epg' not in line:
        if re.search(pattern, line):  # 如果行中有任意关键字
         l.write(line)  # 将该行写入输出文件

         

############
file_contents = []
file_paths = ["a.txt", "b.txt", "d.txt", "c.txt", "e.txt", "e1.txt", "f.txt", "f1.txt", "g.txt", "h.txt", "i.txt", "k.txt", "h1.txt",  "k1.txt",  "j.txt",  "m.txt",  \
              "n.txt",  "o.txt", "l.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的文件
with open("去重.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))

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

# 计算去重前的行数和去重后的行数
original_count = len(lines)
unique_count = len(unique_lines)

# 将唯一的行写入新的文档
with open('结果.txt', 'w', encoding="utf-8") as file:
    file.writelines(unique_lines)

# 输出去重前后的行数
print(f"去重前的行数：{original_count}")
print(f"去重后的行数：{unique_count}")





os.remove("a.txt")
os.remove("b.txt")
os.remove("c.txt")
os.remove("d.txt")
os.remove("2.txt")
os.remove("e.txt")
os.remove("e1.txt")
os.remove("f.txt")
os.remove("f1.txt")
os.remove("g.txt")
os.remove("h.txt")
os.remove("h1.txt")
os.remove("k1.txt")
os.remove("i.txt")
os.remove("j.txt")
os.remove("k.txt")
os.remove("m.txt")
os.remove("n.txt")
os.remove("o.txt")
os.remove("l.txt")
os.remove("去重.txt")
print("任务运行完毕")






