import wx
from Interface.MyFrame import MyFrame
import asyncio


class MyApp(wx.App):

    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        self.keepGoing = True
        return True

    async def MainLoop(self):

        evtloop = wx.GUIEventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)

        while self.keepGoing:

            while evtloop.Pending():
                evtloop.Dispatch()

            await asyncio.sleep(0.0001)

            evtloop.ProcessIdle()

        wx.EventLoop.SetActive(old)

    async def is_scanning(self):

        await asyncio.sleep(0.00001)
        if self.frame.panel.is_scanning:

            return 'True'

        else:

            return 'False'

    def finish_scanning(self):
        self.frame.panel.finish_scanning()

    def update_data(self, *args):

        self.frame.panel.canvas.room.update_model_data(args[0], args[1], args[2], args[3])
