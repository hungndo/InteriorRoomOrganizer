import wx
from Interface.MyCanvas import MyCanvas
from Interface.Furniture import Furniture
from Interface.MyCheckBoxDialog import MyCheckBoxDialog
from Interface.MyRadioDialog import MyRadioDialog


class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("#336B87")

        self.canvas = MyCanvas(self)

        self.is_scanning = False

        self.btn_scan = wx.Button(self, -1, label ="New Scan", pos=(850, 100), size=(135, 50))
        self.btn_scan.SetBackgroundColour("#90AFC5")
        self.btn_load = wx.Button(self, -1, label ="Load", pos=(850, 180), size=(135, 50))
        self.btn_load.SetBackgroundColour("#90AFC5")
        self.btn_save = wx.Button(self, -1, label ="Save", pos=(850, 260), size=(135, 50))
        self.btn_save.SetBackgroundColour("#90AFC5")
        self.btn_add_furniture = wx.Button(self, -1, label="Add Furniture", pos=(850, 340), size=(135, 50))
        self.btn_add_furniture.SetBackgroundColour("#90AFC5")
        self.btn_move_furniture = wx.Button(self, -1, label='Move Furniture', pos=(850, 420), size=(135, 50))
        self.btn_move_furniture.SetBackgroundColour('#90AFC5')
        self.btn_import = wx.Button(self, -1, label="Import Furniture", pos=(850, 500), size=(135, 50))
        self.btn_import.SetBackgroundColour("#90AFC5")

        self.Bind(wx.EVT_BUTTON,self.scan_func, self.btn_scan)
        self.Bind(wx.EVT_BUTTON,self.load_func, self.btn_load)
        self.Bind(wx.EVT_BUTTON,self.save_func, self.btn_save)
        self.Bind(wx.EVT_BUTTON,self.add_furniture_func, self.btn_add_furniture)
        self.Bind(wx.EVT_BUTTON,self.move_furniture_func, self.btn_move_furniture)
        self.Bind(wx.EVT_BUTTON,self.import_func, self.btn_import)

    # --- room functions ---

    def scan_func(self, event):

        self.canvas.create_a_scanning_room()
        self.is_scanning = True

    def load_func(self, event):

        # prevent users from loading another room while scanning
        if not self.is_scanning:

            options = [x for x in self.canvas.room_directories]
            options.append('Nothing')  # since Wx.RadioBox() don't accept empty option list, append 'Nothing'
            dialog = MyRadioDialog(self, 'Choose a room', 'Pick the room that you want to design', options)

            # if there is only one option, which is 'Nothing', set the selected radio button to 'Nothing',
            # and set current_moving_obj to None
            if len(options) == 1:
                dialog.set_selected_option('Nothing')
                self.canvas.change_room('Nothing', False)

            # else set current room to the currently selected radio button
            else:
                tmp = self.canvas.current_room_name
                if tmp is None:
                    dialog.set_selected_option('Nothing')
                else:
                    dialog.set_selected_option(tmp)

            if dialog.ShowModal() == wx.ID_OK:
                self.canvas.change_room(dialog.get_selected_option(), False)

    def save_func(self, event):
        # TODO save a design and prevent users from saving a new design while scanning
        pass

    def finish_scanning(self):

        with wx.TextEntryDialog(self, 'New room', 'Enter the name of your new scanned room', ) as textDialog:

            if textDialog.ShowModal() == wx.CANCEL:
                return

            else:
                room_name = textDialog.GetValue()

                # save the newly scanned room and set it the currently displayed
                self.canvas.room.save_scanned_room(room_name)
                self.canvas.current_room_name = room_name
                self.canvas.add_room_directory(f'../res/Models/rooms/{room_name}/{room_name}.png',
                                               f'../res/Models/rooms/{room_name}/{room_name}.room'.png, room_name)
                self.canvas.change_room(room_name, False)

        self.is_scanning = False

    # --- furniture functions ---

    def import_func(self, event):

        with wx.FileDialog(self, "Import Furniture", style=wx.FD_OPEN | wx.FD_MULTIPLE) as fileDialog:

            # Check if the users changed their minds
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            try:
                read_files = fileDialog.GetPaths()

                # Check if user choose one obj and one png file as required
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
                with wx.TextEntryDialog(self, 'Model name', 'Enter the name of your new model',) as textDialog:

                    if textDialog.ShowModal() == wx.CANCEL:
                        return

                    else:
                        name = textDialog.GetValue()
                        Furniture.save_imported_furniture(read_files, name)

                        if read_files[0].endswith('png'):
                            self.canvas.add_furniture(read_files[0], read_files[1])
                        else:
                            self.canvas.add_furniture(read_files[1], read_files[0])

            except IOError as e:
                wx.LogError(str(e))
                return

            except OSError as e:
                wx.LogError(str(e))
                return

    def add_furniture_func(self, event):

        options = [x for x in self.canvas.furniture]
        dialog = MyCheckBoxDialog(self, 'Select furniture', 'Choose your furniture', options)

        dialog.check_already_selected_options([x for x in self.canvas.furniture if self.canvas.furniture[x].being_shown])

        if dialog.ShowModal() == wx.ID_OK:
            for obj in self.canvas.furniture:
                if obj in dialog.is_checked():
                    self.canvas.furniture[obj].show(True)
                else:
                    self.canvas.furniture[obj].show(False)

        # dialog.Destroy()

    def move_furniture_func(self, event):

        options = [x for x in self.canvas.furniture if self.canvas.furniture[x].being_shown]
        options.append('Nothing')  # since Wx.RadioBox() don't accept empty option list, append 'Nothing'
        dialog = MyRadioDialog(self, 'Move furniture', 'Choose the furniture that you want to move', options)

        # if there is only one option, which is 'Nothing', set the selected radio button to 'Nothing',
        # and set current_moving_obj to None
        if len(options) == 1:
            dialog.set_selected_option('Nothing')
            self.canvas.input.set_current_moving_object(None)
        # else set current_moving_obj to the currently selected one
        else:
            tmp = self.canvas.input.current_obj_key
            if tmp is None:
                dialog.set_selected_option('Nothing')
            else:
                dialog.set_selected_option(tmp)

        if dialog.ShowModal() == wx.ID_OK:
            self.canvas.input.set_current_moving_object(dialog.get_selected_option())
