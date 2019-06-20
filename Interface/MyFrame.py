import sys
import wx
from Interface.MyPanel import MyPanel
from Interface.MyCanvas import MyCanvas


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1000, 700)
        wx.Frame.__init__(self, None ,title ="Interior Room Organizer", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE, pos=(100, 0))
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)
        self.Bind(wx.EVT_CLOSE, self.close_window)

        self.panel = MyPanel(self)

    def close_window(self, event):
        self.Destroy()
        sys.exit(0)
