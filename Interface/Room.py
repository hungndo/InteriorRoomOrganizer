from Interface.Model import Model
import cv2
import numpy


class Room(Model):

    def __init__(self, file):
        
        Model.__init__(self)

        self.vertices = []
        self.textures = []
        self.normals = []
        self.indices = []

        self.texture_data = []
        self.texture_size = (400, 400)

        self.read_model(file)

    def read_model(self, file):

        # read texture
        image = cv2.imread("../res/Models/rooms/3.png", cv2.IMREAD_UNCHANGED)
        # image = cv2.flip(image, 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        # cv2.imshow("f", image)
        for v in range(self.texture_size[1]):
            for u in range(self.texture_size[0]):
                self.texture_data.append(image[u, v])

        self.texture_data = numpy.array(self.texture_data, numpy.uint8)

        # read room
        self.read_room_file(file)

        self.create_vertex_indices_list()

    def read_room_file(self, coordinates_file):
        print('Reading ' + coordinates_file)

        with open(coordinates_file, "r") as file:
            for line in file:
                if not (line.startswith('f') or line.startswith('vn') or line.startswith('vt') or line.startswith('v')):
                        continue

                elif line.startswith('v') and (not (line.startswith('vt') or (line.startswith('vn')))):
                    tmp = line.split()
                    self.vertices.extend(list(map(float, tmp[1:4])))

                elif line.startswith('vt'):
                    tmp = line.split()
                    self.textures.extend(list(map(float, tmp[1:3])))

                elif line.startswith('vn'):
                    tmp = line.split()
                    self.normals.extend(list(map(float, tmp[1:4])))

    def create_vertex_indices_list(self):

        for i in range(len(self.vertices)):
            for j in range(3):
                self.indices.append(i + j)
