#!/usr/bin/python3
#coding=utf-8

# -------------------------------------------------------------------------------
# Filename:    DiagAssistBodyImageTester.py
# Revision:    0.1
# Date:        2018/02/09
# Author:      houfeng
# Description:
# -------------------------------------------------------------------------------

import json
import requests
import ssl
import os
import math
from urllib.request import urlretrieve
from requests import Request, Session
ssl._create_default_https_context = ssl._create_unverified_context
from PIL import  Image
import time
import matplotlib.pyplot as plt
import wx
import base64
from io import BytesIO

G_HTTP = "https"
G_server = "192.168.1.187"
G_PORT = "443"
G_APPNAME = "RLASP7_ONANDON"
G_token = "eyJJc3N1ZWRBdCI6MTUxODMzNDMwMDMwNywiSXNzdWVyIjoiUmVwZWF0bGluayIsIkF1ZGllbmNlIjoiaXBvcyIsInR5cCI6IkpXVCIsImFsZyI6IkhTMjU2IiwiU3ViamVjdCI6IjA5NWRmMjE4LTdhZTctNDg5OC04ZTY3LWRiZTE1YjI0N2U4YiJ9.eyJzaG9wX2lkIjo0LCJjbGllbnRpZCI6IjQiLCJhY2Nlc3NrZXkiOiIxMjNBQkMiLCJwYXlsb2FkIjoie1wiYXV0aF9maWVsZFwiOntcImNsaWVudF9kZXRhaWxfaWRcIjpcIjFcIixcImFjY2Vzc2tleVwiOlwiMTIzQUJDXCIsXCJjbGllbnRpZFwiOlwiNFwifX0iLCJmZWxpY2Fyd3Rvc2hvcF9pZCI6NCwic2NfaWQiOjEsImNsaWVudF9kZXRhaWxfaWQiOiIxIn0.F1A_c3pLXmNvRU8Gqbm9wlYXdpccctZjCR_WPa6vnjE" #Authorization
G_bodyVer = '1.0'
G_clientid = "4"
G_accesskey = "123ABC"
G_client_detail_i = "1"

G_getTokenURL = "/rlapi/authtoken"
G_getVersions = "/rlapi/v3/da/config/version/list"
G_getBodyConfigs = "/rlapi/v3/da/config/bodypart/version"

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}

# G_W = 118
# G_H = 219
#
# G_W = 148
# G_H = 275

G_W = 89
G_H = 165

G_alphaThreshold = 2

overLapPer = 0.3
errorIndexsCount = 0
def getBaseURL():
    return G_HTTP+"://"+G_server+":"+G_PORT+"/"+G_APPNAME
def getToken():
    if os.path.exists('./token.txt'):
        with open('./token.txt','r') as f:
         token = f.read()
         if len(token) > 16:
            G_token = token
            return token
    url = getBaseURL()+G_getTokenURL
    params = {"auth_field":{
          "client_detail_id" : G_clientid,
          "accesskey" : G_accesskey,
          "clientid" : G_client_detail_i
    }}
    jsonParams =  json.dumps(params)

    res = requests.post(url,data=jsonParams,verify=False)
    if res.status_code == 200 :
        results = json.loads(res.text)
        token =  results['results']['result_datas']
        G_token = token
        with open('./token.txt','w') as f:
            f.write(token)
        return token
    return res.text


def getHeaders():
    header_dict['Authorization'] = G_token
    return header_dict

def getDiagAssistVersion():
    if os.path.exists('./bodyver.txt'):
        with open('./bodyver.txt','r') as f:
         ver = f.read()
         if len(ver) > 0:
            G_bodyVer = ver
            return ver
    url = getBaseURL()+G_getVersions
    headers = getHeaders()
    res = requests.get(url,verify=False,headers=headers)
    if res.status_code == 200 :
        results = json.loads(res.text)
        bodyVersions = results['results']['result_datas']['bodypart_version']
        G_bodyVer = bodyVersions
        if bodyVersions :
            with open('./bodyver.txt','w') as f:
                f.write(bodyVersions)
            return bodyVersions

    return res.text

def getBodyConfigs():
    if os.path.exists('./bodyconfig.txt'):
        with open('./bodyconfig.txt','r',encoding='utf8') as f:
         configs = f.read()
         if len(configs) > 0:
            return configs
    url = getBaseURL()+G_getBodyConfigs+'/'+G_bodyVer
    headers = getHeaders()
    res = requests.get(url,verify=False,headers=headers)
    if res.status_code == 200 :
        results = json.loads(res.text)
        configs = results['results']['result_datas']['muscle_infos']
        configsJosnStr = json.dumps(configs,indent=4,ensure_ascii=False)
        if configs :
            with open('./bodyconfig.txt','w',encoding='utf8') as f:
                f.write(configsJosnStr)
            return configsJosnStr

    return res.text

class Rect():
    def __init__(self,x=-1,y=-1,width=-1,height=-1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def toDict(self):
        return {"x":self.x,
                "y":self.y,
                "width":self.width,"height":self.height}
    def isNull(self):
        return self.x == -1 and self.y == -1 and self.width == -1
    def __str__(self):
        return "{"+"x:" + str(self.x) + ",y:"+str(self.y)+",width:"+str(self.width)+",height:"+str(self.height) +"}"

class MuscleInfo():
    def __init__(self):
        self.code = "-1"
        self.name = ""
        self.front = Rect()
        self.back =  Rect()
        self.left = Rect()
        self.right = Rect()

        self.frontSet = []
        self.backSet = []
        self.leftSet = []
        self.rightSet = []

    def toDict(self):
        info  = {}
        # info["code"] = self.code
        # info["name"] = self.name
        # info["front"] = self.front.toDict()
        # info["back"] = self.back.toDict()
        # info["left"] = self.left.toDict()
        # info["right"] = self.right.toDict()

        if len(self.frontSet):
            info['front'] = self.frontSet
        if len(self.backSet):
            info['back'] = self.backSet
        if len(self.leftSet):
            info['left'] = self.leftSet
        if len(self.rightSet):
            info['right'] = self.rightSet

        return info

class MuscleSet():
    def __init__(self):
        self.muscles = []
    def append(self,ms):
        self.muscles.append(ms)
    def toDict(self):
        dic = {}
        for ms in self.muscles:
           if ms.code != None and ms.code != "-1":
            dic[ms.code] = ms.toDict()
        return dic



def downloadImages():
    if not os.path.exists('./images'):
        os.mkdir('./images')
    muscle = json.loads(getBodyConfigs())
    imgNameSet = set()

    totalImgCount = 0
    for i in muscle:
        front_image_url = i['discomfort_image_resources']['front_image_url']
        if front_image_url and front_image_url != "":
            front_image_name = front_image_url.split('/')[-1]
            if front_image_name in imgNameSet:
                print(front_image_name + " 已经重复")
            imgNameSet.add(front_image_name)
            print(front_image_url)
            totalImgCount = totalImgCount + 1
            ir = requests.get(front_image_url)
            if ir.status_code == 200:
                with open("./images/"+front_image_name,'wb') as f:
                    f.write(ir.content)
            else:
                print(front_image_name + "没有下载成功")

        left_image_url = i['discomfort_image_resources']['left_image_url']
        if left_image_url and left_image_url != "":
            left_image_name = left_image_url.split('/')[-1]
            if left_image_name in imgNameSet:
                print(left_image_name + " 已经重复")
            imgNameSet.add(left_image_url)
            print(left_image_url)
            totalImgCount = totalImgCount + 1
            ir = requests.get(left_image_url)
            if ir.status_code == 200:
                with open("./images/"+left_image_name,'wb') as f:
                    f.write(ir.content)
            else:
                print(left_image_name + "没有下载成功")

        right_image_url = i['discomfort_image_resources']['right_image_url']
        if right_image_url and right_image_url != "":
            right_image_name = right_image_url.split('/')[-1]
            if right_image_name in imgNameSet:
                print(right_image_name + " 已经重复")
            print(right_image_url)
            totalImgCount = totalImgCount + 1
            ir = requests.get(right_image_url)
            if ir.status_code == 200:
                with open("./images/"+right_image_name,'wb') as f:
                    f.write(ir.content)
            else:
                print(right_image_name + "没有下载成功")
        back_image_url = i['discomfort_image_resources']['back_image_url']
        if back_image_url and back_image_url != "":
            back_image_name = back_image_url.split('/')[-1]
            if back_image_name in imgNameSet:
                print(back_image_name + " 已经重复")
            print(back_image_url)
            totalImgCount = totalImgCount + 1
            ir = requests.get(back_image_url)
            if ir.status_code == 200:
                with open("./images/"+back_image_name,'wb') as f:
                    f.write(ir.content)
            else:
                print(back_image_name + "没有下载成功")
    print("total image count    : " ,totalImgCount)



def findImageRect(img):
    rect = Rect()
    arrs = []
    w = G_W
    h = G_H
    alphaThreshold = G_alphaThreshold
    if img:
        minX = w
        maxX = 0
        minY = h
        maxY = 0

        newImg = img.resize((w,h))
        for y in range(h):
            for x in range(w):
                rgba  = newImg.getpixel((x,y))
                if rgba[3] > alphaThreshold:
                    index = (w * y + x) * 4
                    arrs.append(index)
                    if x < minX:
                        minX = x
                    if x > maxX :
                        maxX = x
                    if y < minY:
                        minY = y
                    if y > maxY:
                        maxY = y

        rect.x = minX
        rect.y = minY
        rect.width = maxX - minX
        rect.height = maxY - minY

        if rect.width < 0 or rect.height < 0:
            print(rect)
            # print("find image edge error")
            rect = Rect()

    return rect,arrs

def RGB_SquareDistance(rgba1,rgba2):
    return math.pow(rgba1[0]-rgba2[0],2) + math.pow(rgba1[1]-rgba2[1],2) + math.pow(rgba1[2]-rgba2[2],2)


def createImageAlphaIndexs():
    muscle = json.loads(getBodyConfigs())
    msSet = MuscleSet()
    for i in muscle:
        msInfo = MuscleInfo()
        msInfo.code = i['code']
        msInfo.name = i['name']
        msSet.append(msInfo)
        print("deal with ",i['name'])
        front_image_url = i['discomfort_image_resources']['front_image_url']
        if front_image_url and front_image_url != "":
            front_image_name = front_image_url.split('/')[-1]
            img = Image.open("./images/"+front_image_name)
            msInfo.front = findImageRect(img)[0]
            msInfo.frontSet =  findImageRect(img)[1]
            if len(findImageRect(img)[1]) <= errorIndexsCount:
                print("error img :" +front_image_url)
        left_image_url = i['discomfort_image_resources']['left_image_url']
        if left_image_url and left_image_url != "":
            left_image_name = left_image_url.split('/')[-1]
            img = Image.open("./images/"+left_image_name)
            msInfo.left  = findImageRect(img)[0]
            msInfo.leftSet =  findImageRect(img)[1]
            if len(findImageRect(img)[1]) <= errorIndexsCount:
                print("error img :" + left_image_url)
        right_image_url = i['discomfort_image_resources']['right_image_url']
        if right_image_url and right_image_url != "":
            right_image_name = right_image_url.split('/')[-1]
            img = Image.open("./images/"+right_image_name)
            msInfo.right  = findImageRect(img)[0]
            msInfo.rightSet =  findImageRect(img)[1]
            if len(findImageRect(img)[1]) <= errorIndexsCount:
                print("error img :" + right_image_url)

        back_image_url = i['discomfort_image_resources']['back_image_url']
        if back_image_url and back_image_url != "":
            back_image_name = back_image_url.split('/')[-1]
            img = Image.open("./images/"+back_image_name)
            msInfo.back  = findImageRect(img)[0]
            msInfo.backSet =  findImageRect(img)[1]
            if len(findImageRect(img)[1]) <= errorIndexsCount:
                print("error img :" + back_image_url)

    rectDict = msSet.toDict()
    rectJsonStr = json.dumps(rectDict)
    with open('discomfort_image_index_infos.json','w') as f:
        f.write(rectJsonStr)
    return rectDict

def findMacthedImages(targetImg,direction,rectDict):
    rect,indexs = findImageRect(targetImg)
    print("targetImg rect: " , rect)
    print("targetImg indexs: " ,indexs)
    targetImgSet = set(indexs)
    targetImgIndexCount = len(targetImgSet)
    if targetImgIndexCount == 0:
        return []
    findImgCount = 0
    muscle = json.loads(getBodyConfigs())
    imgNames = []
    for i in muscle:
        urlkey = direction + "_image_url"
        image_url = i['discomfort_image_resources'][urlkey]
        code = i['code']
        key = direction
        arr = []
        muscleDic = rectDict[code]
        if key in muscleDic:
            arr = muscleDic[key]
        if arr != None :
            imgIndexSet = set(arr)
            imgCount = len(imgIndexSet)
            if imgCount == 0:
                continue
            intersectionSet = targetImgSet.intersection(imgIndexSet)
            overLapCount = len(intersectionSet)

            per =  float(overLapCount) / float(imgCount)
            targetPer =  float(overLapCount) / float(targetImgIndexCount)
            if per > overLapPer and targetPer > 0.0001:
                findImgCount = findImgCount + 1
                print('find ' + image_url)
                name = image_url.split('/')[-1]
                imgNames.append(name)


    print("total find " + str(findImgCount) + " images")
    return imgNames

def showResult(imgNames):
    dstImg = Image.open('./DA_Karute_body_front.png')
    for imgName in imgNames:
        img = Image.open("./images/"+imgName)
        # if img.size[0] > 592:
        #     img = img.resize((592,1100))
        dstImg.paste(img,mask=img)
    dstImg.save('./dstimg.png','PNG')
    fig = plt.figure(figsize=(4,6))
    ax = fig.add_subplot(111)
    ax.imshow(dstImg)
    plt.show()





if __name__ == '__main__':
    print(getBaseURL())
    print(getToken())
    print(getDiagAssistVersion())
    print(getBodyConfigs())
    downloadImages()
    createImageAlphaIndexs()
    with open('discomfort_image_index_infos.json','r') as f:
        rectDict = json.loads(f.read())
    targetImg = Image.open("back1.png")
    start = time.clock()
    imgNames = findMacthedImages(targetImg,'front',rectDict)
    # imgNames2 = findMacthedImages(targetImg,'back',rectDict)
    # imgNames3 = findMacthedImages(targetImg,'left',rectDict)
    # imgNames4 = findMacthedImages(targetImg,'right',rectDict)
    end = time.clock()
    print("time: %f s" % (end - start))

    showResult(imgNames)

    # targetImg = Image.open("da_search_test1.png")
    # buffered = BytesIO()
    # targetImg.save(buffered, format="PNG")
    # img_str = base64.b64encode(buffered.getvalue())
    # img_str = str(img_str,'utf-8')
    # with open('./testbase64.txt','w') as f:
    #     f.write(img_str)
    # print(img_str)
