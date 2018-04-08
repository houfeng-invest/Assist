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
from urllib.request import urlretrieve
from requests import Request, Session
ssl._create_default_https_context = ssl._create_unverified_context
from PIL import  Image
import time
import matplotlib.pyplot as plt
import wx


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

overLapPer = 0.25
errorIndexsCount = 10
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
        info["code"] = self.code
        # info["name"] = self.name
        # info["front"] = self.front.toDict()
        # info["back"] = self.back.toDict()
        # info["left"] = self.left.toDict()
        # info["right"] = self.right.toDict()

        if len(self.frontSet):
            info['frontSet'] = self.frontSet
        if len(self.backSet):
            info['backSet'] = self.backSet
        if len(self.leftSet):
            info['leftSet'] = self.leftSet
        if len(self.rightSet):
            info['rightSet'] = self.rightSet

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
    for i in muscle:
        front_image_url = i['discomfort_image_resources']['front_image_url']
        if front_image_url and front_image_url != "":
            front_image_name = front_image_url.split('/')[-1]
            print(front_image_url)
            ir = requests.get(front_image_url)
            if ir.status_code == 200:
                with open("./images/"+front_image_name,'wb') as f:
                    f.write(ir.content)

        left_image_url = i['discomfort_image_resources']['left_image_url']
        if left_image_url and left_image_url != "":
            left_image_name = left_image_url.split('/')[-1]
            print(left_image_url)
            ir = requests.get(left_image_url)
            if ir.status_code == 200:
                with open("./images/"+left_image_name,'wb') as f:
                    f.write(ir.content)
        right_image_url = i['discomfort_image_resources']['right_image_url']
        if right_image_url and right_image_url != "":
            right_image_name = right_image_url.split('/')[-1]
            print(right_image_url)
            ir = requests.get(right_image_url)
            if ir.status_code == 200:
                with open("./images/"+right_image_name,'wb') as f:
                    f.write(ir.content)
        back_image_url = i['discomfort_image_resources']['back_image_url']
        if back_image_url and back_image_url != "":
            back_image_name = back_image_url.split('/')[-1]
            print(back_image_url)
            ir = requests.get(back_image_url)
            if ir.status_code == 200:
                with open("./images/"+back_image_name,'wb') as f:
                    f.write(ir.content)



def findImageRect(img):
    rect = Rect()
    arrs = []
    w = G_W
    h = G_H
    if img:
        minX = w
        maxX = 0
        minY = h
        maxY = 0

        newImg = img.resize((w,h))
        for y in range(h):
            for x in range(w):
                rgba  = newImg.getpixel((x,y))
                if rgba[3] > 0:
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

    rectDict = {}
    rectDict['discomfort_image_rect_infos']  = msSet.toDict()
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
    findImgCount = 0
    muscle = json.loads(getBodyConfigs())
    imgNames = []
    for i in muscle:
        urlkey = direction + "_image_url"
        image_url = i['discomfort_image_resources'][urlkey]
        code = i['code']
        key = direction + 'Set'
        arr = []
        muscleDic = rectDict['discomfort_image_rect_infos'][code]
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
            if per > overLapPer :
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
        dstImg.paste(img,mask=img)
    dstImg.save('./dstimg.png','PNG')
    fig = plt.figure(figsize=(4,6))
    ax = fig.add_subplot(111)
    ax.imshow(dstImg)
    plt.show()


class PaintWindow(wx.Window):
        def __init__(self, parent, id):
            wx.Window.__init__(self, parent, id)
            self.color = "Green"
            self.thickness = 10

            #创建一个画笔
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
            self.lines = []
            self.curLine = []
            self.pos = (0, 0)
            self.InitBuffer()

            #连接事件
            self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            self.Bind(wx.EVT_MOTION, self.OnMotion)
            self.Bind(wx.EVT_SIZE, self.OnSize)
            self.Bind(wx.EVT_IDLE, self.OnIdle)
            self.Bind(wx.EVT_PAINT, self.OnPaint)

        def InitBuffer(self):
            size = self.GetClientSize()

            #创建缓存的设备上下文
            self.buffer = wx.EmptyBitmap(size.width, size.height)
            dc = wx.BufferedDC(None, self.buffer)

            #使用设备上下文
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DrawLines(dc)
            self.reInitBuffer = False

        def GetLinesData(self):
            return self.lines[:]

        def SetLinesData(self, lines):
            self.lines = lines[:]
            self.InitBuffer()
            self.Refresh()

        def OnLeftDown(self, event):
            self.curLine = []

            #获取鼠标位置
            self.pos = event.GetPositionTuple()
            self.CaptureMouse()

        def OnLeftUp(self, event):
            if self.HasCapture():
                self.lines.append((self.color,
                                   self.thickness,
                                   self.curLine))
                self.curLine = []
                self.ReleaseMouse()

        def OnMotion(self, event):
            if event.Dragging() and event.LeftIsDown():
                dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
                self.drawMotion(dc, event)
            event.Skip()

        def drawMotion(self, dc, event):
            dc.SetPen(self.pen)
            newPos = event.GetPositionTuple()
            coords = self.pos + newPos
            self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.pos = newPos

        def OnSize(self, event):
            self.reInitBuffer = True

        def OnIdle(self, event):
            if self.reInitBuffer:
                self.InitBuffer()
                self.Refresh(False)

        def OnPaint(self, event):
            dc = wx.BufferedPaintDC(self, self.buffer)

        def DrawLines(self, dc):
            for colour, thickness, line in self.lines:
                pen = wx.Pen(colour, thickness, wx.SOLID)
                dc.SetPen(pen)
                for coords in line:
                    dc.DrawLine(*coords)

        def SetColor(self, color):
            self.color = color
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

        def SetThickness(self, num):
            self.thickness = num
            self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

class PaintFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Panit Frame", size = (592*2+100, 1100))
        self.paint = PaintWindow(self, -1)

# class BodyMap(wx.Frame):
#     def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title=""):
#         wx.Frame.__init__(self, None, id=-1, title="Body Map", pos=wx.DefaultPosition, size=(592*2+100, 1100))
#         self.ms = []
#         front_image = "DA_Karute_body_front.png"
#         self.front = wx.Image(front_image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
#         wx.StaticBitmap(parent=self, bitmap=self.front)
#         self.panel = wx.Panel(parent=self, id=11, pos=(0, 0), size=(592*2+100, 1100))

class BodyMap(wx.Frame):
    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title=""):
        wx.Frame.__init__(self, None, id=-1, title="Body Map", pos=wx.DefaultPosition, size=(1024, 768))

class App(wx.App):
    def OnInit(self):
        self.frame = BodyMap()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    # print(getBaseURL())
    # print(getToken())
    # print(getDiagAssistVersion())
    # print(getBodyConfigs())
    # downloadImages()
    # createImageAlphaIndexs()
    # with open('discomfort_image_index_infos.json','r') as f:
    #     rectDict = json.loads(f.read())
    # targetImg = Image.open("da_search_test2.png")
    # start = time.clock()
    # imgNames = findMacthedImages(targetImg,'front',rectDict)
    # # imgNames2 = findMacthedImages(targetImg,'back',rectDict)
    # # imgNames3 = findMacthedImages(targetImg,'left',rectDict)
    # # imgNames4 = findMacthedImages(targetImg,'right',rectDict)
    # end = time.clock()
    # print("time: %f s" % (end - start))
    #
    # showResult(imgNames)
    print("test")
    app = App()
    app.MainLoop()
