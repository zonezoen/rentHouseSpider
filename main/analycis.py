from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba.analyse
import matplotlib.pyplot as plt
from scipy.misc import imread

baseUrl = "http://sz.zu.fang.com"
import time
from pymongo import MongoClient


class Analycis:
    def __init__(self):
        self.client = MongoClient('mongodb://123.207.242.77:37017/')
        self.zfdb = self.client.zfdb
        self.zfdb.authenticate("zf", "123qweasd!")

    pinyinDir = {
        "不限": "rent",
        "宝安": "baoan",
        "龙岗": "longgang",
        "南山": "nanshan",
        "福田": "futian",
        "罗湖": "luohu",
        "盐田": "yantian",
        "龙华": "longhuaqu",
        "坪山": "pingshanqu",
        "光明": "guangmingxinqu",
        "大鹏": "dapengxinqu",
    }

    def getAreaList(self):
        return [
            "不限",
            "福田",
            "南山",
            "罗湖",
            "宝安",
            "龙华",
            "盐田",
            "龙岗",
            "坪山",
            "光明",
            "大鹏",
        ]

    # 获取区的拼音
    def getPinyin(self, region):
        try:
            pinyin = self.pinyinDir[region]
        except:
            print("no such region pinyin")
        return pinyin

    # 求一个区的  平方米/元  的平均数
    def getAvgPrice(self, region):
        areaPinYin = self.getPinyin(region=region)
        collection = self.zfdb[areaPinYin]
        totalPrice = collection.aggregate([{'$group': {'_id': '$region', 'total_price': {'$sum': '$price'}}}])
        totalArea = collection.aggregate([{'$group': {'_id': '$region', 'total_area': {'$sum': '$area'}}}])
        # totalNum = collection.aggregate([{'$group': {'_id': '$region', 'total_area': {'$sum': 1}}}])
        totalPrice2 = list(totalPrice)[0]["total_price"]
        totalArea2 = list(totalArea)[0]["total_area"]
        return totalPrice2 / totalArea2

    # 获取各个区 每个月一平方米需要多少钱
    def getTotalAvgPrice(self):
        totalAvgPriceList = []
        totalAvgPriceDirList = []

        for index, region in enumerate(self.getAreaList()):
            avgPrice = self.getAvgPrice(region)
            totalAvgPriceList.append(round(avgPrice, 3))
            totalAvgPriceDirList.append({"value": round(avgPrice, 3), "name": region + "  " + str(round(avgPrice, 3))})

        return totalAvgPriceDirList

    # 获取各个区 每一天一平方米需要多少钱
    def getTotalAvgPricePerDay(self):
        totalAvgPriceList = []
        for index, region in enumerate(self.getAreaList()):
            avgPrice = self.getAvgPrice(region)
            totalAvgPriceList.append(round(avgPrice / 30, 3))
        return (self.getAreaList(), totalAvgPriceList)

    # 获取各区统计数据量
    def getAnalycisNum(self):
        analycisList = []
        for index, region in enumerate(self.getAreaList()):
            collection = self.zfdb[self.pinyinDir[region]]
            print(region)
            totalNum = collection.aggregate([{'$group': {'_id': '', 'total_num': {'$sum': 1}}}])
            totalNum2 = list(totalNum)[0]["total_num"]
            analycisList.append(totalNum2)
        return (self.getAreaList(), analycisList)

    # 获取各个区的房源比重
    def getAreaWeight(self):
        result = self.zfdb.rent.aggregate([{'$group': {'_id': '$region', 'weight': {'$sum': 1}}}])
        areaName = []
        areaWeight = []
        for item in result:
            if item["_id"] in self.getAreaList():
                areaWeight.append(item["weight"])
                areaName.append(item["_id"])
                print(item["_id"])
                print(item["weight"])
                # print(type(item))
        return (areaName, areaWeight)

    # 获取 title 数据，用于构建词云
    def getTitle(self):
        collection = self.zfdb["rent"]
        queryArgs = {}
        projectionFields = {'_id': False, 'title': True}  # 用字典指定
        searchRes = collection.find(queryArgs, projection=projectionFields).limit(1000)
        content = ''
        for result in searchRes:
            print(result["title"])
            content += result["title"]
        return content

    # 获取户型数据（3 室 2 厅）
    def getRooms(self):
        results = self.zfdb.rent.aggregate([{'$group': {'_id': '$rooms', 'weight': {'$sum': 1}}}])
        roomList = []
        weightList = []
        for result in results:
            roomList.append(result["_id"])
            weightList.append(result["weight"])
        # print(list(result))
        return (roomList, weightList)

    # 获取租房面积
    def getAcreage(self):
        results0_30 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 0, '$lte': 30}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results30_60 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 30, '$lte': 60}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results60_90 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 60, '$lte': 90}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results90_120 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 90, '$lte': 120}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results120_200 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 120, '$lte': 200}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results200_300 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 200, '$lte': 300}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results300_400 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 300, '$lte': 400}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results400_10000 = self.zfdb.rent.aggregate([
            {'$match': {'area': {'$gt': 300, '$lte': 10000}}},
            {'$group': {'_id': '', 'count': {'$sum': 1}}}
        ])
        results0_30_ = list(results0_30)[0]["count"]
        results30_60_ = list(results30_60)[0]["count"]
        results60_90_ = list(results60_90)[0]["count"]
        results90_120_ = list(results90_120)[0]["count"]
        results120_200_ = list(results120_200)[0]["count"]
        results200_300_ = list(results200_300)[0]["count"]
        results300_400_ = list(results300_400)[0]["count"]
        results400_10000_ = list(results400_10000)[0]["count"]
        attr = ["0-30平方米", "30-60平方米", "60-90平方米", "90-120平方米", "120-200平方米", "200-300平方米", "300-400平方米", "400+平方米"]
        value = [
            results0_30_, results30_60_, results60_90_, results90_120_, results120_200_, results200_300_, results300_400_, results400_10000_
        ]
        return (attr, value)

    # 展示饼图
    def showPie(self, title, attr, value):
        from pyecharts import Pie
        pie = Pie(title)
        pie.add("aa", attr, value, is_label_show=True)
        pie.render()

    # 展示矩形树图
    def showTreeMap(self, title, data):
        from pyecharts import TreeMap
        data = data
        treemap = TreeMap(title, width=1200, height=600)
        treemap.add("深圳", data, is_label_show=True, label_pos='inside', label_text_size=19)
        treemap.render()

    # 展示条形图
    def showLine(self, title, attr, value):
        from pyecharts import Bar
        bar = Bar(title)
        bar.add("深圳", attr, value, is_convert=False, is_label_show=True, label_text_size=18, is_random=True,
                # xaxis_interval=0, xaxis_label_textsize=9,
                legend_text_size=18, label_text_color=["#000"])
        bar.render()

    # 展示词云
    def showWorkCloud(self, content, image_filename, font_filename, out_filename):
        d = path.dirname(__name__)
        # content = open(path.join(d, filename), 'rb').read()
        # 基于TF-IDF算法的关键字抽取, topK返回频率最高的几项, 默认值为20, withWeight
        # 为是否返回关键字的权重
        tags = jieba.analyse.extract_tags(content, topK=100, withWeight=False)
        text = " ".join(tags)
        # 需要显示的背景图片
        img = imread(path.join(d, image_filename))
        # 指定中文字体, 不然会乱码的
        wc = WordCloud(font_path=font_filename,
                       background_color='black',
                       # 词云形状，
                       mask=img,
                       # 允许最大词汇
                       max_words=400,
                       # 最大号字体，如果不指定则为图像高度
                       max_font_size=100,
                       # 画布宽度和高度，如果设置了msak则不会生效
                       # width=600,
                       # height=400,
                       margin=2,
                       # 词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1
                       prefer_horizontal=0.9
                       )
        wc.generate(text)
        img_color = ImageColorGenerator(img)
        plt.imshow(wc.recolor(color_func=img_color))
        plt.axis("off")
        plt.show()
        wc.to_file(path.join(d, out_filename))

    # 展示 pyecharts 的词云
    def showPyechartsWordCloud(self, attr, value):
        from pyecharts import WordCloud
        wordcloud = WordCloud(width=1300, height=620)
        wordcloud.add("", attr, value, word_size_range=[20, 100])
        wordcloud.render()




analycis = Analycis()

# analycis.getTitle()
# analycis.showWorkCloud(analycis.getTitle(), "docker.jpeg", "kh.ttf", out_filename="output.jpeg")

# 统计租房面积
# (attr, value) = analycis.getAcreage()
# analycis.showPie("租房面积统计", attr, value)

# 户型统计
# (attr, value) = analycis.getRooms()
# analycis.showLine("户型统计", attr, value)

# 获取每月每平方米多少钱
data = analycis.getTotalAvgPrice()
print(data)
analycis.showTreeMap("深圳各区房租单价：平方米/月", data)

# 获取每日每平方米多少钱
# (attr, value) = analycis.getTotalAvgPricePerDay()
# print(attr, value)
# analycis.showLine(title="深圳各区房租单价：平方米/日", attr=attr, value=value)

# 样本数量统计
# (attr, value) = analycis.getAnalycisNum()
# print(attr, value)
# analycis.showLine(title="统计样本数量", attr=attr, value=value)

# 房源分布
# (attr, value) = analycis.getAreaWeight()
# print(attr, value)
# analycis.showPie("深圳房源分布", attr, value)
