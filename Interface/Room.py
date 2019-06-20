from Interface.Model import Model
# from Interface.InputManager import *


class Room(Model):

    def __init__(self, coordinates_file):
        
        Model.__init__(self)
        self.read_data_from_file(coordinates_file)
        self.create_vertex_indices_list()

    def read_data_from_file(self, coordinates_file):
        print('Reading ' + coordinates_file)

        file = open(coordinates_file, "r")

        for line in file:
            split_line = line.split()

            self.vertices.append(float(split_line[0]))
            self.vertices.append(-float(split_line[2]))
            self.vertices.append(float(split_line[1]))

            self.colors.append(float(split_line[4])/256)
            self.colors.append(float(split_line[5])/256)
            self.colors.append(float(split_line[6])/256)

        file.close()

    def create_vertex_indices_list(self):

        for i in range(len(self.vertices)):
            for j in range(3):
                self.indices.append(i + j)



