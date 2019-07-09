import wx
from Interface.MyCanvas import MyCanvas
import os
import cv2


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__( self, parent)
        self.SetBackgroundColour("#252525")

        self.canvas = MyCanvas(self)

        self.is_scanning = False

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

        self.is_scanning = True

    def load_func(self, event):

        with wx.FileDialog(self, "Load existing design",
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

        with wx.FileDialog(self, "Import Furniture", style=wx.FD_OPEN | wx.FD_MULTIPLE) as fileDialog:

            # Check if the users changed their minds
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # Check if user choose one obj and one png file as required
            try:
                read_files = fileDialog.GetPaths()
                if not(len(read_files) == 2):
                    raise IOError('You need two load one obj file and one png file.')
                else:
                    if read_files[0].endswith('png') or read_files[0].endswith('jpg'):
                        if not read_files[1].endswith('obj'):
                            raise IOError('You need two load one obj file and one png file.')

                    elif read_files[0].endswith('obj'):
                        if not (read_files[1].endswith('png') or read_files[1].endswith('jpg')):
                            raise IOError('You need two load one obj file and one png file.')

                    else:
                        raise IOError('You need two load one obj file and one png file.')

                # create a new directory for the new furniture
                with wx.TextEntryDialog(self, 'Model name','Enter the name of your new model',) as textDialog:

                    if textDialog.ShowModal() == wx.CANCEL:
                        return

                    else:
                        name = textDialog.GetValue()
                        if not os.path.exists(f'../res/Models/furniture/{name}'):
                            os.mkdir(f'../res/Models/furniture/{name}')

                # copy selected files to the new folder
                obj_file = f'../res/Models/furniture/{name}/{name}.obj'
                png_file = f'../res/Models/furniture/{name}/{name}.png'
                if read_files[0].endswith('obj'):

                    # copy obj file
                    with open(read_files[0], 'r') as readfile:
                        with open(obj_file, 'w') as writefile:
                            writefile.writelines(readfile.read())

                    # copy png file
                    img = cv2.imread(read_files[1], cv2.IMREAD_UNCHANGED)
                    read_files[1] = cv2.imwrite(png_file, img)

                else:
                    print('here')
                    # copy png file
                    img = cv2.imread(read_files[1], cv2.IMREAD_UNCHANGED)
                    read_files[1] = cv2.imwrite(png_file, img)

                    # copy obj file
                    with open(read_files[1], 'r') as readfile:
                        with open(obj_file, 'w') as writefile:
                            writefile.writelines(readfile.read())

            except IOError as e:
                wx.LogError(str(e))
                return

            except OSError as e:
                wx.LogError(str(e))
                return

    def add_furniture_func(self,event):

        with wx.Dialog(self, title = "Choose", size = (400,400)) as dialog:
            dialog.ShowModal()
            button = wx.Button(dialog, -1, label ="ABC", size = (100,100), pos = (200,200))
