import wx


class MyCheckBoxDialog(wx.Dialog):

    def __init__(self, parent, title, message, options = []):

        wx.Dialog.__init__(self, parent, -1)

        self.SetTitle(title)
        self.message = wx.StaticText(self, -1, message)
        self.checklist = wx.CheckListBox(self, -1, choices = options)
        self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        self.select_all_box = wx.CheckBox(self,-1, 'Select all')

        self.Bind(wx.EVT_CHECKBOX, self.select_all_func, self.select_all_box)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.message, 0, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.checklist, 1, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.select_all_box, 0, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.buttons, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(self.sizer)

    def select_all_func(self,evt):
        for i in range(self.checklist.GetCount()):
            self.checklist.Check(i, self.select_all_box.IsChecked())

    def is_checked(self):
        return self.checklist.GetCheckedStrings()

    def check_already_selected_options(self, string_list):
        self.checklist.SetCheckedStrings(string_list)

