from Interface.Model import Model
import cv2
import numpy
import os


class Room(Model):

    def __init__(self, png_file=None, room_file=None, new_scan=False):
        
        Model.__init__(self)

        self.vertex_coords = []
        self.texture_coords = []
        self.normal_coords = []
        self.indices = []

        self.texture_data = []
        self.texture_size = (400, 400)

        if not new_scan:
            self.read_model(png_file, room_file)

    def read_model(self, png_file, room_file):

        # read texture
        image = cv2.imread(png_file, cv2.IMREAD_UNCHANGED)
        image = cv2.flip(image, 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        for v in range(self.texture_size[1]):
            for u in range(self.texture_size[0]):
                self.texture_data.append(image[u, v])

        self.texture_data = numpy.array(self.texture_data, numpy.uint8)

        # read room
        self.read_room_file(room_file)

        self.create_vertex_indices_list()

    def read_room_file(self, coordinates_file):
        print('Reading ' + coordinates_file)

        with open(coordinates_file, "r") as file:
            for line in file:
                if not (line.startswith('f') or line.startswith('vn') or line.startswith('vt') or line.startswith('v')):
                        continue

                elif line.startswith('v') and (not (line.startswith('vt') or (line.startswith('vn')))):
                    tmp = line.split()
                    self.vertex_coords.extend(list(map(float, tmp[1:4])))

                elif line.startswith('vt'):
                    tmp = line.split()
                    self.texture_coords.extend(list(map(float, tmp[1:3])))

                elif line.startswith('vn'):
                    tmp = line.split()
                    self.normal_coords.extend(list(map(float, tmp[1:4])))

    def create_vertex_indices_list(self):

        for i in range(len(self.vertex_coords)):
            for j in range(3):
                self.indices.append(i + j)

###########

    def save_scanned_room(self, room_name):

        if not os.path.exists(f'../res/Models/rooms/{room_name}'):
            os.mkdir(f'../res/Models/rooms/{room_name}')

        try:

            # copy selected files to the new folder
            room_file = f'../res/Models/rooms/{room_name}/{room_name}.room'
            png_file = f'../res/Models/rooms/{room_name}/{room_name}.png'
            super.create_png_image(png_file, self.texture_data)
            super.create_room_file(room_file, self.vertex_coords, self.texture_coords, self.normal_coords)

        except IOError as e:
            print(e)
