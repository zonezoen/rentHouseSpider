from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba.analyse
import matplotlib.pyplot as plt
from scipy.misc import imread


def showWorkCloud(filename, image_filename, font_filename, out_filename):
    d = path.dirname(__name__)
    content = open(path.join(d, filename), 'rb').read()

    print(content)
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
                   # mask=color_mask,
                   # 允许最大词汇
                   max_words=400,
                   # 最大号字体，如果不指定则为图像高度
                   max_font_size=100,
                   # 画布宽度和高度，如果设置了msak则不会生效
                   width=600,
                   height=400,
                   margin=2,
                   # 词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1
                   prefer_horizontal=0.8
                   )
    wc.generate(text)
    img_color = ImageColorGenerator(img)
    plt.imshow(wc.recolor(color_func=img_color))
    plt.axis("off")
    plt.show()
    wc.to_file(path.join(d, out_filename))
    return


class cloud:
    def __init__(self, filename, image_filename, font_filename, ou):
        self.d = path.dirname(__name__)
        content = open(path.join(self.d, filename), 'rb').read()
        # 基于TF-IDF算法的关键字抽取, topK返回频率最高的几项, 默认值为20, withWeight
        # 为是否返回关键字的权重
        tags = jieba.analyse.extract_tags(content, topK=100, withWeight=False)
        self.text = " ".join(tags)
        # 需要显示的背景图片
        self.img = imread(path.join(self.d, image_filename))
        # 指定中文字体, 不然会乱码的
        self.wc = WordCloud(font_path=font_filename,
                            background_color='black',
                            # 词云形状，
                            # mask=color_mask,
                            # 允许最大词汇
                            max_words=400,
                            # 最大号字体，如果不指定则为图像高度
                            max_font_size=100,
                            # 画布宽度和高度，如果设置了msak则不会生效
                            width=600,
                            height=400,
                            margin=2,
                            # 词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1
                            prefer_horizontal=0.8
                            )
        self.wc.generate(self.text)

    def show_wc(self):
        '''显示生成的词云图'''
        # 让词的颜色和图片的颜色一样
        img_color = ImageColorGenerator(self.img)
        plt.imshow(self.wc.recolor(color_func=img_color))
        plt.axis("off")
        plt.show()

    def save_wc(self, out_filename):
        '''保存到当前目录下'''
        self.wc.to_file(path.join(self.d, out_filename))


if __name__ == '__main__':
    # wc = cloud("comment.txt", "aa.jpeg", "kh.ttf")
    # wc.show_wc()
    # wc.save_wc('output.jpg')
    showWorkCloud("comment.txt", "docker.jpeg", "kh.ttf",'output.jpg')
