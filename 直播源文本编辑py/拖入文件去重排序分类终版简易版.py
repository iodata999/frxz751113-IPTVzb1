from pypinyin import lazy_pinyin
import re
import os
from opencc import OpenCC

# 提示用户输入文件名（拖入文件操作）
file_path = input('FileName(DragHere): ')

# 检查文件是否存在
if not os.path.isfile(file_path):
    print("文件不存在，请重新输入.")
    exit(1)

# 打开用户指定的文件
with open(file_path, 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()

# 定义一个函数，用于提取每行的第一个数字
def extract_first_number(line):
    match = re.search(r'\d+', line)
    return int(match.group()) if match else float('inf')

# 对列表中的行进行排序
# 按照第一个数字的大小排列，如果不存在数字则按中文拼音排序
sorted_lines = sorted(lines, key=lambda x: (not 'CCTV' in x, extract_first_number(x) if 'CCTV' in x else lazy_pinyin(x.strip())))

# 将排序后的行写入新的utf-8编码的文本文件，文件名基于原文件名
output_file_path = "sorted_" + os.path.basename(file_path)

# 写入新文件
with open('2.txt', "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line)

print(f"文件已排序并保存为: {output_file_path}")



################简体转繁体
# 创建一个OpenCC对象，指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('2.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()

# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)

# 将转换后的简体字写入txt文件
with open('2.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)



def check_and_write_file(input_file, output_file, keywords):
    # 使用 split(',') 而不是 split(', ') 来分割关键词
    keywords_list = keywords.split(',')
    first_keyword = keywords_list[0]  # 获取第一个关键词作为头部信息

    pattern = '|'.join(re.escape(keyword) for keyword in keywords_list)
    extracted_lines = False

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(f'{first_keyword},#genre#\n')  # 使用第一个关键词作为头部信息

        for line in lines:
            if 'genre' not in line and 'epg' not in line:
                if re.search(pattern, line):
                    out_file.write(line)
                    extracted_lines = True

    # 如果没有提取到任何关键词，则不保留输出文件
    if not extracted_lines:
        os.remove(output_file)  # 删除空的输出文件
        print(f"未提取到关键词，{output_file} 已被删除。")
    else:
        print(f"文件已提取关键词并保存为: {output_file}")

# 按类别提取关键词并写入文件
check_and_write_file('2.txt', 'a.txt', keywords="央视频道,CCTV,风云音乐,CGTN,CETV,女性,4k,4K,8K,8k,地理,风云剧场,怀旧剧场,第一剧场,家庭,影迷,高清电影,动作电影,CHC,世界地理,兵器,央视台球,第一剧场,风云足球,高尔夫,\
动作电影,家庭影院,影迷电影,星光,华语,峨眉,世界地理")

check_and_write_file('2.txt', 'b.txt', keywords="卫视频道,卫视,星空,凤凰")

check_and_write_file('2.txt', 'c.txt', keywords="影视频道,爱情喜剧,爱喜喜剧,惊嫊悬疑,东北热剧,都市剧场,海外剧场,欢笑剧场,重温经典,军事评论,农业致富,哒啵赛事,怡伴健康,明星大片,武博世界,HOT,\
中国功夫,军旅,炫舞未来,精品体育,精品萌宠,精品记录,超级体育,超级,金牌,东北热剧,中国功夫,军旅剧场,古装剧场,家庭剧场,惊悚悬疑,欢乐剧场,潮妈辣婆,爱情喜剧,精品大剧,超级影视,超级电影,黑莓动画,黑莓电影,\
海外剧场,精彩影视,七彩戏剧,东方影视,无名影视,潮婆辣妈,超级剧,热播精选,武术世界,求索动物,求索,求索科学,求索记录,爱谍战,爱动漫,爱科幻,爱青春,爱科学,爱浪漫,爱历史,爱旅行,爱奇谈,爱怀旧,爱赛车,爱体育,爱经典,\
爱玩具,爱喜剧,爱悬疑,爱幼教,爱院线,精品纪录")

check_and_write_file('2.txt', 'd.txt', keywords="少儿频道,少儿,卡通,动漫,宝贝,哈哈")

check_and_write_file('2.txt', 'e.txt', keywords="港澳频道,TVB,澳门,龙华,民视,中视,华视,耀才,公视,寰宇,无线,EVEN,MoMo,爆谷,面包,momo,唐人,中华小,三立,CNA,FOX,RTHK,Movie,八大,中天,中视,东森,凤凰,天映,美亚,\
环球,翡翠,亚洲,大爱,大愛,明珠,半岛,AMC,龙祥,台视,1905,纬来,神话,经典都市,视界,番薯,私人,酒店,TVB,凤凰,半岛,星光视界,番薯,大愛,新加坡,星河,明珠,环球,翡翠台")





check_and_write_file('2.txt', 'f.txt', keywords="湖北湖南,湖北,武汉,松滋,十堰,咸宁,远安,黄石,荆州,当阳,恩施,五峰,来凤,枝江,黄冈,随州,荆门,秭归,孝感,\
鄂州,湖北,五峰,来凤,枝江,随州,荆门,秭归,孝感,鄂州,武汉,松滋,十堰,咸宁,黄石,垄上,荆州,当阳,恩施,宜都")
check_and_write_file('2.txt', 'f1.txt', keywords="湖北湖南,湖南,长沙,常德,郴州,衡阳,怀化,吉首,娄底,邵阳,湘潭,益阳,永州,岳阳,张家界,株洲")



check_and_write_file('2.txt', 'g.txt', keywords="浙江上海,浙江,杭州,宁波,丽水,上虞,舟山,新密,衢州,嘉兴,绍兴,温州,湖州,永嘉,诸暨,钱江,松阳,苍南,遂昌,青田,龙泉,余杭,新昌,杭州,余杭,丽水,龙泉,\
青田,松阳,遂昌,宁波,余姚,上虞,新商都,绍兴,温州,永嘉,诸暨,钱江,金华,苍南")
check_and_write_file('2.txt', 'g1.txt', keywords="浙江上海,上海,东方,东方财经,五星体育,崇明")




check_and_write_file('2.txt', 'h.txt', keywords="河南河北,河南,焦作,封丘,郏县,获嘉,巩义,邓州,宝丰,开封,卢氏,洛阳,孟津,安阳,渑池,南阳,内黄,平顶山,淇县,杞县,汝阳,三门峡,\
卫辉,淅川,新密,新乡,信阳,新郑,延津,叶县,义马,永城,禹州,原阳,镇平,郑州,周口")
check_and_write_file('2.txt', 'h1.txt', keywords="河南河北,河北,石家庄,承德,丰宁,临漳,井陉,井陉矿区,保定,元氏,兴隆,内丘,南宫,吴桥,唐县,唐山,安平,定州,大厂,张家口,徐水,成安,\
故城,康保,廊坊,晋州,景县,武安,枣强,柏乡,涉县,涞水,涞源,涿州,深州,深泽,清河,秦皇岛,衡水,遵化,邢台,邯郸,邱县,隆化,雄县,\
阜平,高碑店,高邑,魏县,黄骅,饶阳,赵县,睛彩河北,滦南,玉田,崇礼,平泉,容城,文安,三河,清河")







check_and_write_file('2.txt', 'i.txt', keywords="江苏江西,江苏,常州,淮安,连云港,南京,南通,高邮,苏州,宿迁,泰州,无锡,徐州,盐城,扬州,镇江")
check_and_write_file('2.txt', 'i1.txt', keywords="江苏江西,江西,抚州,赣州,吉安,景德镇,九江,南昌,萍乡,上饶,新余,宜春,鹰潭")



check_and_write_file('2.txt', 'j.txt', keywords="广东广西,广东,潮州,东莞,佛山,广州,河源,惠州,江门,揭阳,茂名,梅州,清远,汕头,汕尾,韶关,深圳,阳江,云浮,湛江,肇庆,中山,珠海")
check_and_write_file('2.txt', 'j1.txt', keywords="广东广西,广西,百色,北海,防城港,桂林,河池,柳州,南宁,钦州,梧州,玉林")





check_and_write_file('2.txt', 'k.txt', keywords="山东山西,山东,滨州,德州,东营,菏泽,济南,济宁,莱芜,聊城,临沂,青岛,日照,泰安,威海,潍坊,烟台,枣庄,淄博,山西,长治,大同,晋城,\
晋中,临汾,吕梁,朔州,太原,忻州,阳泉,运城")




check_and_write_file('2.txt', 'l.txt', keywords="安徽四川,安徽,安庆,蚌埠,亳州,巢湖,池州,滁州,阜阳,合肥,淮北,淮南,黄山,六安,马鞍山,宿州,铜陵,芜湖,宣城")
check_and_write_file('2.txt', 'l1.txt', keywords="安徽四川,四川,阿坝,巴中,成都,达州,德阳,甘孜,广安,广元,乐山,凉山,泸州,眉山,绵阳,内江,南充,攀枝花,遂宁,雅安,宜宾,资阳,自贡,黑水,\
金川,乐至,双流,万源,马尔康,泸县,文山,什邡,西青,长宁,达州,红河")




check_and_write_file('2.txt', 'm.txt', keywords="其他频道,,")





############
file_contents = []
file_paths = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "f1.txt", "g.txt", "g1.txt", "h.txt", "h1.txt", "i.txt", "i1.txt", "j.txt", "j1.txt", "k.txt", "l.txt", "l1.txt", "m.txt",  \
              "n.txt", "o.txt", "p.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
    else:                # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file_path} 不存在，跳过")
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
with open('分类.txt', 'w', encoding="utf-8") as file:
    file.writelines(unique_lines)

# 输出去重前后的行数
print(f"去重前的行数：{original_count}")
print(f"去重后的行数：{unique_count}")





#任务结束，删除不必要的过程文件###########################################################################################################################
files_to_remove = ['去重.txt', "2.txt","a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt", "f1.txt", "g.txt", "g1.txt", "h.txt", "h1.txt", "i.txt", "i1.txt", "j.txt", "j1.txt", "k.txt", "l.txt", "l1.txt", "m.txt",  \
              "n.txt", "o.txt", "p.txt" ]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")

print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")




