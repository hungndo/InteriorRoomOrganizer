from Interface.Model import Model
from Interface.Transform import Transform
import numpy
import cv2
import os


class Furniture(Model, Transform):

    def __init__(self, texture_file, obj_file):

        Model.__init__(self)
        Transform.__init__(self)

        self.being_shown = False

        self.ROTATE_SPEED = 0.3
        self.moving_speed = 0.1
        self.scale = 30

        self.vertex_coords = []
        self.texture_coords = []
        self.normal_coords = []
        self.indices = []

        self.texture_data = []
        self.texture_size = ()

        self.read_model(texture_file, obj_file)

    def read_model(self, texture_file, obj_file):

        # read texture
        image = cv2.imread(texture_file, cv2.IMREAD_UNCHANGED)
        self.texture_size = image.shape
        image = cv2.flip(image, 0)

        # since open-cv reads image files in BGRA, we need to convert it to RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        for v in range(self.texture_size[0]):
            for u in range(self.texture_size[1]):
                self.texture_data.append(image[v, u])

        self.texture_data = numpy.array(self.texture_data, numpy.uint8)

        # read obj
        self.read_obj_file(obj_file)

    def read_obj_file(self, obj_file):

        tmp_vertices = []
        tmp_textures = []
        tmp_normals = []
        index_count = 0     # this variable to to create the indices_list, however, I am not using it now

        with open(obj_file, 'r') as file:
            for line in file:
                if not (line.startswith('f') or line.startswith('vn') or line.startswith('vt') or line.startswith('v')):
                    continue

                elif line.startswith('v') and (not (line.startswith('vt') or (line.startswith('vn')))):
                    tmp = line.split()
                    tmp_vertices.append(list(map(float, tmp[1:4])))

                elif line.startswith('vt'):
                    tmp = line.split()
                    tmp_textures.append(list(map(float,tmp[1:3])))

                elif line.startswith('vn'):
                    tmp = line.split()
                    tmp_normals.append(list(map(float, tmp[1:4])))

                elif line.startswith('f'):

                    tmp = line.split()
                    for i in range(1,4):

                        self.indices.append(index_count)
                        index_count += 1
                        t = tmp[i].split('/')
                        for q in range(len(t)):
                            if t[q] == '':
                                t[q] = 0
                        x = list(map(int, t))
                        self.refine_vertices(x, tmp_vertices, tmp_textures, tmp_normals)

    def refine_vertices(self, vertex, tmp_vertices, tmp_textures, tmp_normals):

        # since obj file doesn't give vertex, texture, normal coords in the correct order,
        # this function is to rearrange those

        # each indices is subtracted by 1 because obj format counts from 1

        self.vertex_coords.extend(tmp_vertices[vertex[0]-1])
        self.texture_coords.extend(tmp_textures[vertex[1]-1])
        self.normal_coords.extend(tmp_normals[vertex[2]-1])

    @staticmethod
    def save_imported_furniture(read_files, name):

        if not os.path.exists(f'../res/Models/furniture/{name}'):
            os.mkdir(f'../res/Models/furniture/{name}')

        # copy selected files to the new folder

        obj_file = f'../res/Models/furniture/{name}/{name}.obj'
        png_file = f'../res/Models/furniture/{name}/{name}.png'

        try:
            if read_files[0].endswith('obj'):

                # copy obj file
                with open(read_files[0], 'r') as readfile:
                    with open(obj_file, 'w') as writefile:
                        writefile.writelines(readfile.read())

                # copy png file
                img = cv2.imread(read_files[1], cv2.IMREAD_UNCHANGED)
                cv2.imwrite(png_file, img)

            else:
                # copy png file
                img = cv2.imread(read_files[1], cv2.IMREAD_UNCHANGED)
                cv2.imwrite(png_file, img)

                # copy obj file
                with open(read_files[1], 'r') as readfile:
                    with open(obj_file, 'w') as writefile:
                        writefile.writelines(readfile.read())

        except IOError as e:
            print(e)

    def show(self, state):
        self.being_shown = state

    def is_shown(self):
        return self.being_shown

    # TODO move objects by dragging mouse
    def move_left(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_left()

    def move_right(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_right()

    def move_inward(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_inward()

    def move_outward(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_outward()

    def move_up(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_up()

    def move_down(self, moving_speed = None):
        # self.moving_speed = moving_speed
        super().move_down()
