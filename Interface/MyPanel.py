import wx
from Interface.MyCanvas import MyCanvas


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__( self, parent)
        self.SetBackgroundColour("#626D56")

        self.canvas = MyCanvas(self)
        self.rot_btn = wx.Button(self, -1, label ="Rotate", pos=(0, 0), size=(50, 700))

