#!/usr/bin/python3
#coding=utf-8



import  os
from PIL import  Image

'''
如何判断是同一张图片呢？最简单的方法是使用加密哈希（例如MD5, SHA-1）判断。但是局限性非常大。例如一个txt文档，其MD5值是根据这个txt的二进制数据计算的，如果是这个txt文档的完全复制版，那他们的MD5值是完全相同的。但是，一旦改变副本的内容，哪怕只是副本的缩进格式，其MD5也会天差地别。因此加密哈希只能用于判断两个完全一致、未经修改的文件，如果是一张经过调色或者缩放的图片，根本无法判断其与另一张图片是否为同一张图片。
那么如何判断一张被PS过的图片是否与另一张图片本质上相同呢？比较简单、易用的解决方案是采用感知哈希算法（Perceptual Hash Algorithm)。

感知哈希算法是一类算法的总称，包括aHash、pHash、dHash。顾名思义，感知哈希不是以严格的方式计算Hash值，而是以更加相对的方式计算哈希值，因为“相似”与否，就是一种相对的判定。

    aHash：平均值哈希。速度比较快，但是常常不太精确。
    pHash：感知哈希。精确度比较高，但是速度方面较差一些。
    dHash：差异值哈希。Amazing！精确度较高，且速度也非常快。因此我就选择了dHash作为我图片判重的算法。

一、 相似图片检测步骤：

    分别计算两张图片的dHash值
    通过dHash值计算两张图片的汉明距离（Hamming Distance），通过汉明距离的大小，判断两张图片的相似程度。


Step1. 缩放图片

如果我们要计算上图的dHash值，第一步是把它缩放到足够小。为什么需要缩放呢？因为原图的分辨率一般都非常高。一张 200*200 的图片，就有整整4万个像素点，每一个像素点都保存着一个RGB值，4万个RGB，是相当庞大的信息量，非常多的细节需要处理。因此，我们需要把图片缩放到非常小，隐藏它的细节部分，只见森林，不见树木。建议缩放为9*8，虽然可以缩放为任意大小，但是这个值是相对合理的。而且宽度为9，有利于我们转换为hash值

dHash全名为差异值hash，通过计算相邻像素之间的颜色强度差异得出。我们缩放后的图片，细节已经被隐藏，信息量已经变少。但是还不够，因为它是彩色的，由RGB值组成。白色表示为（255,255,255）,黑色表示为（0,0,0），值越大颜色越亮，越小则越暗。每种颜色都由3个数值组成，也就是红、绿、蓝的值 。如果直接使用RGB值对比颜色强度差异，相当复杂，因此我们转化为灰度值——只由一个0到255的整数表示灰度。这样的话就将三维的比较简化为了一维比较。

差异值是通过计算每行相邻像素的强度对比得出的。我们的图片为9*8的分辨率，那么就有8行，每行9个像素。差异值是每行分别计算的，也就是第二行的第一个像素不会与第一行的任何像素比较。每一行有9个像素，那么就会产生8个差异值，这也是为何我们选择9作为宽度，因为8bit刚好可以组成一个byte，方便转换为16进制值。
如果前一个像素的颜色强度大于第二个像素，那么差异值就设置为True（也就是1），如果不大于第二个像素，就设置为False（也就是0）。


我们将差异值数组中每一个值看做一个bit，每8个bit组成为一个16进制值，将16进制值连接起来转换为字符串，就得出了最后的dHash值。


汉明距离这个概念不止运用于图片对比领域，也被使用于众多领域，具体的介绍可以参见Wikipedia。
汉明距离表示将A修改成为B，需要多少个步骤。比如字符串“abc”与“ab3”，汉明距离为1，因为只需要修改“c”为“3”即可。
dHash中的汉明距离是通过计算差异值的修改位数。我们的差异值是用0、1表示的，可以看做二进制。二进制0110与1111的汉明距离为2。
我们将两张图片的dHash值转换为二进制difference，并取异或。计算异或结果的“1”的位数，也就是不相同的位数，这就是汉明距离。


'''
from PIL import  Image

class DHash(object):
    @staticmethod
    def calculate_hash(image):
        """
        计算图片的dHash值
        :param image: PIL.Image
        :return: dHash值,string类型
        """
        difference = DHash.__difference(image)
        # 转化为16进制(每个差值为一个bit,每8bit转为一个16进制)
        decimal_value = 0
        hash_string = ""
        for index, value in enumerate(difference):
            if value:  # value为0, 不用计算, 程序优化
                decimal_value += value * (2 ** (index % 8))
            if index % 8 == 7:  # 每8位的结束
                hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
                decimal_value = 0
        return hash_string

    @staticmethod
    def hamming_distance(first, second):
        """
        计算两张图片的汉明距离(基于dHash算法)
        :param first: Image或者dHash值(str)
        :param second: Image或者dHash值(str)
        :return: hamming distance. 值越大,说明两张图片差别越大,反之,则说明越相似
        """
        # A. dHash值计算汉明距离
        if isinstance(first, str):
            return DHash.__hamming_distance_with_hash(first, second)

        # B. image计算汉明距离
        hamming_distance = 0
        image1_difference = DHash.__difference(first)
        image2_difference = DHash.__difference(second)
        for index, img1_pix in enumerate(image1_difference):
            img2_pix = image2_difference[index]
            if img1_pix != img2_pix:
                hamming_distance += 1
        return hamming_distance

    @staticmethod
    def __difference(image):
        """
        *Private method*
        计算image的像素差值
        :param image: PIL.Image
        :return: 差值数组。0、1组成
        """
        resize_width = 9
        resize_height = 8
        # 1. resize to (9,8)
        smaller_image = image.resize((resize_width, resize_height))
        # 2. 灰度化 Grayscale
        grayscale_image = smaller_image.convert("L")
        # 3. 比较相邻像素
        pixels = list(grayscale_image.getdata())
        difference = []
        for row in range(resize_height):
            row_start_index = row * resize_width
            for col in range(resize_width - 1):
                left_pixel_index = row_start_index + col
                difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
        return difference

    @staticmethod
    def __hamming_distance_with_hash(dhash1, dhash2):
        """
        *Private method*
        根据dHash值计算hamming distance
        :param dhash1: str
        :param dhash2: str
        :return: 汉明距离(int)
        """
        difference = (int(dhash1, 16)) ^ (int(dhash2, 16))
        return bin(difference).count("1")
