from Interface.Model import Model
from Interface.Transform import Transform
import numpy
import cv2


class Furniture(Model, Transform):

    def __init__(self):

        Model.__init__(self)
        Transform.__init__(self)

        self.ROTATE_SPEED = 0.3

        self.vertices = []
        self.textures = []
        self.normals = []
        self.indices = []

        self.texture_data = []
        self.texture_size = (256, 256)

        self.read_model()

    def read_model(self):

        # read texture
        image = cv2.imread("../res/stallTexture.png", cv2.IMREAD_UNCHANGED)
        image = cv2.flip(image, 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        for v in range(self.texture_size[0]):
            for u in range(self.texture_size[1]):
                self.texture_data.append(image[v, u])

        self.texture_data = numpy.array(self.texture_data, numpy.uint8)
        # read obj
        self.read_obj_file()

    def read_obj_file(self):

        tmp_vertices = []
        tmp_textures = []
        tmp_normals = []
        index_count = 0

        with open("../res/stall.obj", 'r') as file:
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
                        x = list(map(int,tmp[i].split('/')))
                        self.refine_vertices(x, tmp_vertices, tmp_textures, tmp_normals)

    def refine_vertices(self, vertex, tmp_vertices, tmp_textures, tmp_normals):

        # each indices is subtracted by 1 because obj format counts from 1

        self.vertices.extend(tmp_vertices[vertex[0]-1])
        self.textures.extend(tmp_textures[vertex[1]-1])
        self.normals.extend(tmp_normals[vertex[2]-1])

    def move_left(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_left()

    def move_right(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_right()

    def move_inward(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_inward()

    def move_outward(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_outward()

    def move_up(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_up()

    def move_down(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_down()
