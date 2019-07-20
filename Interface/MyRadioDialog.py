import wx


class MyRadioDialog(wx.Dialog):

    def __init__(self, parent, title, message, options = []):

        wx.Dialog.__init__(self, parent, -1)

        self.SetTitle(title)
        self.message = wx.StaticText(self, -1, message)
        self.radiolist = wx.RadioBox(self, -1, choices = options, style = wx.VERTICAL)
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.message, 0, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.radiolist, 1, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.buttons, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(self.sizer)

    def get_selected_option(self):
        selected_index = self.radiolist.GetSelection()
        return self.radiolist.GetString(selected_index)

    def set_selected_option(self, option):

        index = self.radiolist.FindString(option)
        self.radiolist.SetSelection(index)
