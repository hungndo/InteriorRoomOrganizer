import wx
from wx.glcanvas import *


class MyCanvas(GLCanvas):

    def __init__(self, parent):
        GLCanvas.__init__(self, parent, -1, size=(1000, 700))
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        print("HI")
        self.Refresh()

class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1000, 700)
        wx.Frame.__init__(self, None, title ="Interior Room Organizer", size=self.size)
        self.canvas = MyCanvas(self)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    # app = MyApp()
    # app.MainLoop()
    app = wx.App(False)
    frame = wx.Frame(None, title = "GLCanvas")
    canvas = MyCanvas(frame)
    frame.Show()
    app.MainLoop()



