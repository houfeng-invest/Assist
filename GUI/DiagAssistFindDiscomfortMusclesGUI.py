#!/usr/bin/python3
# -*- coding: UTF-8 -*-



import wx
import os
from PIL import Image

front_image = "da_front.png"
back_image = "DA_Karute_body_front.png"


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
            print(f)


class BodyMap(wx.Frame):
    c1 = None
    c2 = None

    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title=""):
        wx.Frame.__init__(self, None, id=-1, title="Body Map", pos=wx.DefaultPosition, size=(592 + 100, 1100 / 2 + 50))
        self.ms = []
        self.selectedImg = None

        temp = wx.Image(front_image, wx.BITMAP_TYPE_PNG)
        w, h = temp.GetWidth() / 2, temp.GetHeight() / 2
        self.w = w
        self.h = h
        print(w, h)
        self.back = wx.Image(back_image, wx.BITMAP_TYPE_PNG).Scale(w, h).ConvertToBitmap()
        self.front = wx.Image(front_image, wx.BITMAP_TYPE_PNG).Scale(w, h).ConvertToBitmap()

        wx.StaticBitmap(parent=self, bitmap=self.front)
        wx.StaticBitmap(parent=self, bitmap=self.back, pos=(592 / 2 + 100, 0))

        self.color = "Green"
        self.thickness = 10

        # 创建一个画笔
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)

        # 创建一个画笔
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

        self.posCtrl = wx.TextCtrl(self, -1, "", pos=(900, 700))

        self.fileDrop = FileDrop(self)
        self.SetDropTarget(self.fileDrop)
        self.panel = wx.Panel(parent=self, id=11, pos=(0, 0), size=(w, h))
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.panel.Bind(wx.EVT_MOTION, self.OnMotion)
        self.panel.Bind(wx.EVT_SIZE, self.OnSize)
        self.panel.Bind(wx.EVT_IDLE, self.OnIdle)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)


        # self.panel.Bind(wx.EVT_MOTION, self.OnMouseMove)
        # self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        # self.panel.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        # self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        # self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def GetLinesData(self):
        return self.lines[:]

    def SetLinesData(self, lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()

    def OnLeftDown(self, event):
        self.curLine = []

        # 获取鼠标位置
        self.pos = event.GetPosition()
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
        newPos = event.GetPosition()
        coords = self.pos + newPos
        self.curLine.append(coords)
        dc.DrawLine(*coords)
        self.pos = newPos

    def OnSize(self, event):
        pass
        # self.reInitBuffer = True

    def OnIdle(self, event):
        pass
        # if self.reInitBuffer:
        #     self.InitBuffer()
        #     self.Refresh(False)

    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        brush = wx.Brush(wx.Colour(1,200,0,10))
        dc.SetBackground(brush)
        dc.Clear()
        # self.DrawLines(dc)

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


        # def OnMouseMove(self, event):
        #     if event.Dragging() and event.LeftIsDown():
        #         self.c2 = event.GetPosition()
        #         self.Refresh()
        #
        # def OnMouseDown(self, event):
        #     self.c1 = event.GetPosition()
        #
        # def OnMouseUp(self, event):
        #     self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        #
        # def OnPaint(self, event):
        #     if self.c1 is None or self.c2 is None: return
        #
        #     dc = wx.PaintDC(self.panel)
        #     dc.SetPen(wx.Pen('red', 1))
        #     dc.SetBrush(wx.Brush(self.color, wx.TRANSPARENT))
        #
        #     dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)
        #
        # def PrintPosition(self, pos):
        #     return str(pos.x) + " " + str(pos.y)


class App(wx.App):
    def OnInit(self):
        self.frame = BodyMap()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
