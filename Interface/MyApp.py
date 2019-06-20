import wx
from Interface.MyFrame import MyFrame


class MyApp(wx.App):

    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True
