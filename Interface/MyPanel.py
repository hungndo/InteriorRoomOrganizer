import wx
from Interface.MyCanvas import MyCanvas


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__( self, parent)
        self.SetBackgroundColour("#252525")

        self.canvas = MyCanvas(self)

        self.btn_scan = wx.Button(self, -1, label ="New Scan", pos=(850, 100), size=(135, 50))
        self.btn_scan.SetBackgroundColour("#b5d374")
        self.btn_load = wx.Button(self, -1, label ="Load", pos=(850, 200), size=(135, 50))
        self.btn_load.SetBackgroundColour("#b5d374")
        self.btn_save = wx.Button(self, -1, label ="Save", pos=(850, 300), size=(135, 50))
        self.btn_save.SetBackgroundColour("#b5d374")
        self.btn_add_furniture = wx.Button(self, -1, label="Add Furniture", pos=(850, 400), size=(135, 50))
        self.btn_add_furniture.SetBackgroundColour("#b5d374")
        self.btn_import = wx.Button(self, -1, label="Import Furniture", pos=(850, 500), size=(135, 50))
        self.btn_import.SetBackgroundColour("#b5d374")

        self.Bind(wx.EVT_BUTTON,self.scan_func, self.btn_scan)
        self.Bind(wx.EVT_BUTTON,self.load_func, self.btn_load)
        self.Bind(wx.EVT_BUTTON,self.save_func, self.btn_save)
        self.Bind(wx.EVT_BUTTON,self.add_furniture_func, self.btn_add_furniture)
        self.Bind(wx.EVT_BUTTON,self.import_func, self.btn_import)

    def scan_func(self, event):
        print("scan ")

    def load_func(self, event):
        print("load")

    def save_func(self, event):

        with wx.FileDialog(self, "Save new design", wildcard="XYZ files (*.xyz)|*.xyz",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()

            try:
                with open(pathname, 'w') as file:
                    print("save")
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def import_func(self, event):

        with wx.FileDialog(self, "Import Furniture", wildcard="OBJ files (*.jpg)|*.jpg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    print("Hey")
            except IOError:
                wx.LogError("Cannot open file '%s'." % file)

    def add_furniture_func(self,event):
        print("add")
