from pypinyin import lazy_pinyin
import re
import os
from opencc import OpenCC
import fileinput

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

# 定义替换规则的字典###############规范频道名
replacements = {
    	"CCTV-1高清测试": "",
    	"CCTV-2高清测试": "",
    	"CCTV-7高清测试": "",
    	"CCTV-10高清测试": "",
    	"中央": "CCTV",
    	"高清""": "",
    	"HD": "",
    	"[浙江]": "浙江",
    	"|": "",
    	"」": "",
    	"标清": "",
    	"-": "",
    	"[1080p]": "",
    	"[720p]": "",
    	"[540p]": "",
    	"[210p]": "",
    	"[576p]": "",
    	"$4.0M1080": "",
    	"$5.5M1080": "",
    	"$海南移动V4": "",
    	"$4.1M1080": "",
    	"$8.1M1080": "",
    	"$7.9M1080": "",
    	"$未知480P": "",
    	"$8.0M1080": "",
    	"$7.6M1080": "",
    	"$7.0M1080": "",
    	"$6.9M1080": "",
    	"$7.8M1080": "",
    	"$7.9M_1080": "",
    	"[720*480]": "",
    	"[1280*720]": "",
    	"[1920*1080]": "",
    	"[960*540]": "",
    	"SD": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"": "",
    	"超清": "",
    	"湖南茶": "茶",
    	"湖南金鹰纪实": "金鹰纪实",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	" ": "",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV兵器科技": "兵器科技",
    	"CCTV地理世界": "地理世界",
    	"CCTV风云足球": "风云足球",
    	"CCTV央视台球": "央视台球",
    	"CCTV台球": "台球",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV中视购物": "中视购物",
    	"CCTV发现之旅": "发现之旅",
    	"CCTV中学生": "中学生",
    	"CCTV高尔夫网球": "高尔夫网球",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"熊猫影院": "熊猫电影",
    	"熊猫爱生活": "熊猫生活",
    	"爱宠宠物": "宠物生活",
    	"[ipv6]": "",
    	"专区": "",
    	"卫视超": "卫视",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"IPTV": "",
    	"PLUS": "+",
    	"＋": "+",
    	"(": "",
    	")": "",
    	"CAV": "",
    	"美洲": "",
    	"北美": "",
    	"12M": "",
    	"高清测试CCTV-1": "",
    	"高清测试CCTV-2": "",
    	"高清测试CCTV-7": "",
    	"高清测试CCTV-10": "",
    	"LD": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	"NewTv": "",
    	"NEWTV": "",
    	"NewTV": "",
    	"iHOT": "",
    	"CHC": "",
    	"测试cctv": "CCTV",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"CCTV4国际": "CCTV4",
    	"CCTV4中文国际": "CCTV4",
    	"CCTV4欧洲": "CCTV4",
    	"CCTV5体育": "CCTV5",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV6电影": "CCTV6",
    	"CCTV7军事": "CCTV7",
    	"CCTV7军农": "CCTV7",
    	"CCTV7农业": "CCTV7",
    	"CCTV7国防军事": "CCTV7",
    	"CCTV8电视剧": "CCTV8",
    	"CCTV8影视": "CCTV8",
    	"CCTV8纪录": "CCTV9",
    	"CCTV9记录": "CCTV9",
    	"CCTV9纪录": "CCTV9",
    	"CCTV10科教": "CCTV10",
    	"CCTV11戏曲": "CCTV11",
    	"CCTV12社会与法": "CCTV12",
    	"CCTV13新闻": "CCTV13",
    	"CCTV新闻": "CCTV13",
    	"CCTV14少儿": "CCTV14",
    	"央视14少儿": "CCTV14",
    	"CCTV少儿超": "CCTV14",
    	"CCTV15音乐": "CCTV15",
    	"CCTV音乐": "CCTV15",
    	"CCTV16奥林匹克": "CCTV16",
    	"CCTV17农业农村": "CCTV17",
    	"CCTV17军农": "CCTV17",
    	"CCTV17农业": "CCTV17",
    	"CCTV5+体育赛视": "CCTV5+",
    	"CCTV5+赛视": "CCTV5+",
    	"CCTV5+体育赛事": "CCTV5+",
    	"CCTV5+赛事": "CCTV5+",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV5赛事": "CCTV5+",
    	"凤凰中文台": "凤凰中文",
    	"凤凰资讯台": "凤凰资讯",
    	"(CCTV4K测试）": "CCTV4K",
    	"上海东方卫视": "上海卫视",
    	"东方卫视": "上海卫视",
    	"内蒙卫视": "内蒙古卫视",
    	"福建东南卫视": "东南卫视",
    	"广东南方卫视": "南方卫视",
    	"湖南金鹰卡通": "金鹰卡通",
    	"炫动卡通": "哈哈炫动",
    	"卡酷卡通": "卡酷少儿",
    	"卡酷动画": "卡酷少儿",
    	"BRTVKAKU少儿": "卡酷少儿",
    	"优曼卡通": "优漫卡通",
    	"优曼卡通": "优漫卡通",
    	"嘉佳卡通": "佳嘉卡通",
    	"世界地理": "地理世界",
    	"CCTV世界地理": "地理世界",
    	"BTV北京卫视": "北京卫视",
    	"BTV冬奥纪实": "冬奥纪实",
    	"东奥纪实": "冬奥纪实",
    	"卫视台": "卫视",
    	"湖南电视台": "湖南卫视",
    	"少儿科教": "少儿",
    	"影视剧": "影视",
    	"电视剧": "影视",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}


# 创建新文件并写入替换后的内容
with open('2.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        for old, new in replacements.items():
            line = line.replace(old, new)
        new_file.write(line)

print("替换完成，新文件已保存。")


#################文本排序

# 打开原始文件读取内容，并写入新文件
with open('2.txt', 'r', encoding='utf-8') as file:
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
    # 使用 split(', ') 而不是 split(',') 来分割关键词
    keywords_list = keywords.split(', ')
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
check_and_write_file('2.txt',  'a.txt',  keywords="央视频道, CCTV, 8K, 4k,h, 爱上4K, 纯享, 风云剧场, 怀旧剧场, 影迷, 高清电影, 动作电影, 第一剧场, 家庭影院, 影迷电影, 星光, 华语, 峨眉")
check_and_write_file('2.txt',  'a1.txt',  keywords="央视频道, 文物宝库, 风云音乐, 生活时尚, 台球, 网球, 足球, 女性, 地理, 纪实科教, 纪实人文, 兵器, 北京纪实, 发现, 法治")

check_and_write_file('2.txt',  'b.txt',  keywords="卫视频道, 卫视")

check_and_write_file('2.txt',  'c.txt',  keywords="影视频道, 爱情喜剧, 爱喜喜剧, 惊嫊悬疑, 东北热剧, 无名, 都市剧场, 海外剧场, 欢笑剧场, 重温经典, 明星大片, 中国功夫, 军旅, 东北热剧, 中国功夫, 军旅剧场, 古装剧场, 家庭剧场, 惊悚悬疑, 欢乐剧场, 潮妈辣婆, 爱情喜剧, 精品大剧, 超级影视, 超级电影, 黑莓动画, 黑莓电影, 海外剧场, 精彩影视, 无名影视, 潮婆辣妈, 超级剧, 热播精选")
check_and_write_file('2.txt',  'c1.txt',  keywords="影视频道, 求索动物, 求索, 求索科学, 求索记录, 爱谍战, 爱动漫, 爱科幻, 爱青春, 爱自然, 爱科学, 爱浪漫, 爱历史, 爱旅行, 爱奇谈, 爱怀旧, 爱赛车, 爱体育, 爱经典, 爱玩具, 爱喜剧, 爱悬疑, 爱幼教, 爱院线")
check_and_write_file('2.txt',  'c2.txt',  keywords="影视频道, 军事评论, 农业致富, 哒啵赛事, 怡伴健康, 武博世界, 超级综艺, 哒啵, HOT, 炫舞未来, 精品体育, 精品萌宠, 精品记录, 超级体育, 金牌, 武术世界, 精品纪录")

check_and_write_file('2.txt',  'd.txt',  keywords="少儿频道, 少儿, 卡通, 动漫, 宝贝, 哈哈")

check_and_write_file('2.txt',  'e.txt',  keywords="港澳频道, TVB, 澳门, 龙华, 民视, 中视, 华视, 耀才, 非凡, 公视, 寰宇, 无线, EVEN, MoMo, 爆谷, 面包, momo, 唐人, 中华小, 三立, CNA, FOX, RTHK, Movie, 八大, 中天, 中视, 东森, 凤凰, 天映, 美亚, 环球, 翡翠, 亚洲, 大爱, 大愛, 明珠, 半岛, AMC, 龙祥, 台视, 1905, 纬来, 神话, 经典都市, 视界, 番薯, 私人, 酒店, TVB, 凤凰, 半岛, 星光视界, 番薯, 大愛, 新加坡, 星河, 明珠, 环球, 翡翠台")

#check_and_write_file('2.txt',  'f0.txt',  keywords="湖北湖南, 湖北, 湖南")
check_and_write_file('2.txt',  'f.txt',  keywords="湖北湖南, 湖北, 武汉, 松滋, 十堰, 咸宁, 远安, 崇阳, 黄石, 荆州, 当阳, 恩施, 五峰, 来凤, 枝江, 黄冈, 随州, 荆门, 秭归, 孝感, 鄂州, 湖北, 五峰, 来凤, 枝江, 随州, 荆门, 秭归, 孝感, 鄂州, 武汉, 松滋, 十堰, 咸宁, 黄石, 垄上, 荆州, 当阳, 恩施, 宜都")
check_and_write_file('2.txt',  'f1.txt',  keywords="湖北湖南, 湖南, 长沙, 常德, 郴州, 垂钓, 金鹰纪实, 衡阳, 怀化, 茶, 吉首, 娄底, 邵阳, 湘潭, 益阳, 永州, 岳阳, 张家界, 株洲")

#check_and_write_file('2.txt',  'g0.txt',  keywords="浙江上海, 浙江, 上海")
check_and_write_file('2.txt',  'g.txt',  keywords="浙江上海, 浙江, 杭州, 宁波, 平湖, 庆元, 缙云, 嵊, 义乌, 东阳, 文成, 云和, 象山, 衢江, 萧山, 龙游, 武义, 兰溪, 开化, 丽水, 上虞, NBTV, 舟山, 新密, 衢州, 嘉兴, 绍兴, 温州, 湖州, 永嘉, 诸暨, 钱江, 松阳, 苍南, 遂昌, 青田, 龙泉, 余杭, 新昌, 杭州, 余杭, 丽水, 龙泉, 青田, 松阳, 遂昌, 宁波, 余姚, 上虞, 新商都, 绍兴, 温州, 永嘉, 诸暨, 钱江, 金华, 苍南")
check_and_write_file('2.txt',  'g1.txt',  keywords="浙江上海, 上海, 东方, 普陀, 东方财经, 五星体育, 第一财经, 七彩, 崇明")

#check_and_write_file('2.txt',  'h0.txt',  keywords="河南河北, 河南, 河北")
check_and_write_file('2.txt',  'h.txt',  keywords="河南河北, 河南, 焦作, 封丘, 郏县, 获嘉, 巩义, 邓州, 宝丰, 开封, 卢氏, 洛阳, 孟津, 安阳, 渑池, 南阳, 林州, 滑县, 栾川, 襄城, 宜阳, 长垣, 内黄, 鹿邑, 新安, 平顶山, 淇县, 杞县, 汝阳, 三门峡, 卫辉, 淅川, 新密, 新乡, 信阳, 新郑, 延津, 叶县, 义马, 永城, 禹州, 原阳, 镇平, 郑州, 周口")
check_and_write_file('2.txt',  'h1.txt',  keywords="河南河北, 河北, 石家庄, 承德, 丰宁, 临漳, 井陉, 井陉矿区, 保定, 元氏, 兴隆, 内丘, 南宫, 吴桥, 唐县, 唐山, 安平, 定州, 大厂, 张家口, 徐水, 成安, 故城, 康保, 廊坊, 晋州, 景县, 武安, 枣强, 柏乡, 涉县, 涞水, 涞源, 涿州, 深州, 深泽, 清河, 秦皇岛, 衡水, 遵化, 邢台, 邯郸, 邱县, 隆化, 雄县, 阜平, 高碑店, 高邑, 魏县, 黄骅, 饶阳, 赵县, 睛彩河北, 滦南, 玉田, 崇礼, 平泉, 容城, 文安, 三河, 清河")

check_and_write_file('2.txt',  'i.txt',  keywords="江苏江西, 江苏, 常州, 淮安, 连云港, 南京, 南通, 高邮, 苏州, 江宁, 宿迁, 泰州, 无锡, 徐州, 盐城, 扬州, 镇江")
check_and_write_file('2.txt',  'i1.txt',  keywords="江苏江西, 江西, 抚州, 赣州, 吉安, 景德镇, 九江, 南昌, 萍乡, 上饶, 新余, 宜春, 鹰潭")

#check_and_write_file('2.txt',  'j.txt',  keywords="广东广西, 广东, 广西")
check_and_write_file('2.txt',  'j.txt',  keywords="广东广西, 广东, 潮州, 东莞, 佛山, 广州, 河源, 惠州, 江门, 揭阳, 茂名, 梅州, 清远, 汕头, 汕尾, 韶关, 深圳, 阳江, 云浮, 湛江, 肇庆, 中山, 珠海")
check_and_write_file('2.txt',  'j1.txt',  keywords="广东广西, 广西, 百色, 北海, 防城港, 桂林, 河池, 贺州, 柳州, 南宁, 钦州, 梧州, 玉林")

check_and_write_file('2.txt',  'k.txt',  keywords="山东山西, 山东, 滨州, 青州, 德州, 东营, 菏泽, 济南, 济宁, 莱芜, 聊城, 临沂, 青岛, 日照, 泰安, 威海, 潍坊, 烟台, 枣庄, 淄博, 山西, 长治, 大同, 晋城, 晋中, 临汾, 吕梁, 朔州, 太原, 忻州, 阳泉, 运城")

#check_and_write_file('2.txt',  'l0.txt',  keywords="安徽四川, 安徽, 四川")
check_and_write_file('2.txt',  'l.txt',  keywords="安徽四川, 安徽, 安庆, 蚌埠, 亳州, 巢湖, 池州, 岳西, 滁州, 阜阳, 合肥, 淮北, 淮南, 黄山, 六安, 马鞍山, 宿州, 铜陵, 芜湖, 宣城")
check_and_write_file('2.txt',  'l1.txt',  keywords="安徽四川, 四川, 阿坝, 巴中, 成都, 达州, 德阳, 甘孜, 广安, 广元, 乐山, 凉山, 泸州, 眉山, 绵阳, 内江, 南充, 攀枝花, 遂宁, 雅安, 宜宾, 资阳, 自贡, 黑水, 金川, 乐至, 双流, 万源, 马尔康, 泸县, 文山, 什邡, 西青, 长宁, 达州, 红河")

check_and_write_file('2.txt',  'm.txt',  keywords="云南贵州, 云南, 版纳, 保山, 楚雄, 大理, 德宏, 西畴, 迪庆, 砚山, 红河, 昆明, 丽江, 麻栗坡, 临沧, 怒江, 曲靖, 思茅, 文山, 玉溪, 昭通, 西双版纳")
check_and_write_file('2.txt',  'm1.txt',  keywords="云南贵州, 贵州, 安顺, 毕节, 都匀, 贵阳, 凯里, 六盘水, 铜仁, 兴义, 遵义")

#check_and_write_file('2.txt',  'n0.txt',  keywords="甘肃黑龙江, 甘肃, 黑龙江")
check_and_write_file('2.txt',  'n.txt',  keywords="甘肃黑龙江, 黑龙江, 大庆, 大兴安岭, 哈尔滨, 鹤岗, 黑河, 鸡西, 佳木斯, 牡丹江, 七台河, 齐齐哈尔, 双鸭山, 绥化, 伊春")
check_and_write_file('2.txt',  'n1.txt',  keywords="甘肃黑龙江, 甘肃, 兰州, 蒙古, 海南, 辽宁, 延安, 吴忠, 西宁")

check_and_write_file('2.txt',  'o.txt',  keywords="其他频道, , ")




############
file_contents = []
file_paths = ["a.txt", "a1.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "e.txt", "f0.txt", "f.txt", "f1.txt", "g0.txt", "g.txt", "g1.txt", "h0.txt", "h.txt", "h1.txt", "i.txt", \
              "i1.txt", "j.txt", "j1.txt", "k.txt", "l0.txt", "l.txt", "l1.txt", "m.txt", "m1.txt",  \
              "n0.txt","n.txt","n1.txt", "o.txt", "p.txt"]  # 替换为实际的文件路径列表
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


def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[https]?[http]?[P2p]?[mitv]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))

# 使用方法
remove_duplicates('去重.txt', '分类.txt')

# 打开文档并读取所有行 
with open('分类.txt', 'r', encoding="utf-8") as file:
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
with open('分类.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)





#任务结束，删除不必要的过程文件###########################################################################################################################
files_to_remove = ['去重.txt', "2.txt","a.txt", "a1.txt", "b.txt", "c.txt", "c1.txt", "c2.txt", "d.txt", "e.txt", "f0.txt", "f.txt", "f1.txt", "g0.txt", "g.txt", "g1.txt", "h0.txt", "h.txt", "h1.txt", "i.txt", \
              "i1.txt", "j.txt", "j1.txt", "k.txt", "l0.txt", "l.txt", "l1.txt", "m.txt", "m1.txt",  \
              "n0.txt","n.txt","n1.txt", "o.txt", "p.txt"]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
    else:              # 如果文件不存在，则提示异常并打印提示信息
        print(f"文件 {file} 不存在，跳过删除。")

print("任务运行完毕，分类频道列表可查看文件夹内综合源.txt文件！")




