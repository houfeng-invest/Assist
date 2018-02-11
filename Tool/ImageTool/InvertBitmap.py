#!/usr/bin/python3
#coding=utf-8

# -------------------------------------------------------------------------------
# Filename:    InvertBitmap.py
# Revision:    0.1
# Date:        2018/02/09
# Author:      houfeng
# Description: 反相当前目录下的小票打印logo
# -------------------------------------------------------------------------------


import  os
from PIL import  Image
currentPath = os.path.abspath('.')
def Invert(path):
    for i in os.listdir(path):
        subPath = path+"/"+i
        if os.path.isdir(subPath):
            Invert(subPath)
        elif os.path.splitext(subPath)[1] == '.bmp' or os.path.splitext(subPath)[1] == '.png':
            print("开始反转 %s",i)
            img = Image.open(subPath)
            img = img.convert('1')
            print(img.mode)
            pixels = img.load()
            print(img.getpixel((0,0)))
            w,h = img.size
            print(img.size)
            for i in range(h):
                for j in range(w):
                    oldPixel = pixels[j,i]
                    newPixel = 255 - oldPixel
                    pixels[j,i] = newPixel
                    # print(oldPixel,sep=",",end="")
                # print('\n')
            img.save(subPath)

Invert(currentPath)
