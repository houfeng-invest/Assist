#!/usr/bin/python3
# -*- coding: UTF-8 -*-



import wx
import os
from PIL import Image


front_image = "DA_body_front@2x.png"
back_image = "DA_body_back@2x.png"

class MyImageView():
    def __init__(self, parent=None, bitmap=None, pos=None):
        self.map = parent
        self.selected = False
        self.btn = wx.StaticBitmap(parent=parent, bitmap=bitmap, pos=pos)
        self.text = wx.StaticText(self.btn, wx.ID_ANY, "", (bitmap.GetWidth() / 2 - 5, bitmap.GetHeight() / 2 - 5),
                                  size=(10, 10))
        self.btn.Bind(wx.EVT_RIGHT_UP, self.rightUP)
        self.btn.Bind(wx.EVT_LEFT_DOWN, self.leftClick)
        self.btn.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)
        self.btn.Bind(wx.EVT_MOTION, self.mouseMove)
        self.btn.Bind(wx.EVT_LEFT_UP, self.mouseUp)

        self.curBitmapPostion = None
        self.curPointerPos = None

    def leftClick(self, e):
        pos = self.btn.GetPosition()
        if pos.x > 500:
            pos.x = pos.x - 500
        self.map.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))
        e.Skip()

    def rightUP(self, e):
        pos = self.btn.GetPosition()
        if pos.x > 500:
            pos.x = pos.x - 500
        self.map.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))
        for m in self.map.ms:
            m.text.SetLabelText("")
        self.map.selectedImg = None
        self.selected = not self.selected
        if self.selected:
            self.text.SetLabelText("+")
            self.map.selectedImg = self


        else:
            self.text.SetLabelText("")

        print(self.selected)
        e.Skip()

    # def mouseDown(self, event):
    #     print("------------------------")
    #     pos = event.GetPosition()
    #     if self.selected :
    #         self.curPointerPos = pos
    #         self.curBitmapPostion = self.btn.GetPosition()
    #         self.curBitmapPostion = self.curBitmapPostion + pos
    #         self.btn.SetPosition(self.curBitmapPostion)
    #
    #
    # def mouseMove(self, event):
    #     pos = event.GetPosition()
    #     if self.selected :
    #         if self.curPointerPos != None and self.curBitmapPostion != None:
    #             self.curPointerPos = pos
    #             self.curBitmapPostion = self.btn.GetPosition()
    #             self.curBitmapPostion = self.curBitmapPostion + pos
    #             self.btn.SetPosition(self.curBitmapPostion)
    #
    #
    # def mouseUp(self, event):
    #     self.curBitmapPostion = None
    #     self.curPointerPos = None


class FileDrop(wx.FileDropTarget):
    def __init__(self, map):
        wx.FileDropTarget.__init__(self)
        self.map = map

    def OnDropFiles(self, x, y, filePath):
        for f in filePath:
            if f[-4:] == ".png":
                temp = wx.Image(f, wx.BITMAP_TYPE_PNG)
                w, h = temp.GetWidth() / 2, temp.GetHeight() / 2
                temp = temp.Scale(w, h).ConvertToBitmap()
                btn = MyImageView(parent=self.map, bitmap=temp, pos=(x, y))
                print(btn)
                self.map.ms.append(btn)
            print(f)


class BodyMap(wx.Frame):
    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title=""):

        self.ms = []
        self.selectedImg = None

        temp = wx.Image(front_image, wx.BITMAP_TYPE_PNG)
        w, h = temp.GetWidth() / 2, temp.GetHeight() / 2
        self.back = wx.Image(back_image, wx.BITMAP_TYPE_PNG).Scale(w, h).ConvertToBitmap()
        self.front = wx.Image(front_image, wx.BITMAP_TYPE_PNG).Scale(w, h).ConvertToBitmap()

        wx.Frame.__init__(self, None, id=-1, title="Body Map", pos=wx.DefaultPosition, size=(1024, 768))
        wx.StaticBitmap(parent=self, bitmap=self.front)
        wx.StaticBitmap(parent=self, bitmap=self.back, pos=(500, 0))

        # self.Bind(wx.EVT_MOTION,self.OnMove)

        self.posCtrl = wx.TextCtrl(self, -1, "", pos=(900, 700))

        self.fileDrop = FileDrop(self)
        self.SetDropTarget(self.fileDrop)
        self.panel = wx.Panel(parent=self, id=11, pos=(0, 0), size=(1024, 768))
        # self.Bind(wx.EVT_MOUSE_EVENTS,  self.dragEVT)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)
        self.panel.Bind(wx.EVT_MOTION, self.mouseMove)
        self.panel.Bind(wx.EVT_LEFT_UP, self.mouseUp)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.curBitmapPostion = None
        self.curPointerPos = None

    def mouseDown(self, event):
        pos = event.GetPosition()
        x = pos.x
        if x > 500:
            x = x - 500
        # self.posCtrl.SetValue("%s, %s" % (x, pos.y))
        if self.selectedImg != None:
            self.selectedImg.btn.SetPosition(pos)
            self.curBitmapPostion = self.selectedImg.btn.GetPosition()
        self.curPointerPos = pos
        event.Skip()

    def mouseMove(self, event):
        print("+++++++++++++++++++++++++++++++")
        pos = event.GetPosition()
        x = pos.x
        if x > 500:
            x = x - 500
        # self.posCtrl.SetValue("%s, %s" % (x, pos.y))
        if self.curPointerPos != None and self.curBitmapPostion != None:
            movPos = event.GetPosition() - self.curPointerPos
            print(movPos)
            self.curBitmapPostion = self.curBitmapPostion + movPos
            if self.selectedImg != None:
                self.selectedImg.btn.SetPosition(self.curBitmapPostion)
            self.curPointerPos = self.curBitmapPostion
        event.Skip()

    def mouseUp(self, event):
        pos = event.GetPosition()
        x = pos.x
        if x > 500:
            x = x - 500
        self.curBitmapPostion = None
        self.curPointerPos = None
        event.Skip()

    def OnKeyDown(self, event):
        kc = event.GetKeyCode()
        if kc == 314:
            if self.selectedImg != None:
                pos = self.selectedImg.btn.GetPosition()
                pos.x -= 1
                self.selectedImg.btn.SetPosition(pos)
            print(kc)
        elif kc == 315:
            if self.selectedImg != None:
                pos = self.selectedImg.btn.GetPosition()
                pos.y -= 1
                self.selectedImg.btn.SetPosition(pos)
        elif kc == 316:
            if self.selectedImg != None:
                pos = self.selectedImg.btn.GetPosition()
                pos.x += 1
                self.selectedImg.btn.SetPosition(pos)
        elif kc == 317:
            if self.selectedImg != None:
                pos = self.selectedImg.btn.GetPosition()
                pos.y += 1
                self.selectedImg.btn.SetPosition(pos)
        else:
            print(kc)
        if self.selectedImg != None:
            pos = self.selectedImg.btn.GetPosition()
            x = pos.x
            if x > 500:
                x = x - 500
            self.posCtrl.SetValue("%s, %s" % (x, pos.y))


class App(wx.App):
    def OnInit(self):
        self.frame = BodyMap()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
