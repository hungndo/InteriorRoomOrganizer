from OpenGL.GL import *
from Interface.Shader import Shader
import numpy
import cv2
import os

class Model:

    def __init__(self):

        self.vertex_coords = []
        self.texture_coords = []
        self.normal_coords = []
        self.indices = []

        self.texture_data = None
        self.texture_size = None

        self.shader = None
        self.buffer = None
        self.texture_buffer = None

        self.transform_model_view_loc = None
        self.projection_loc = None

        self.update_awaiting = True

    def create_texture(self):

        self.texture_buffer = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture_buffer)

        # texture wrapping params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # texture filtering params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # image
        glEnable(GL_TEXTURE_2D)

    def create_vbo(self):
        self.buffer = glGenBuffers(4)

    def draw_vbo(self):

        # fetch and pass matrices into shader
        transform_model_view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
        glUniformMatrix4fv(self.transform_model_view_loc, 1, GL_FALSE, transform_model_view_matrix)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection_matrix)

        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # texture
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        # normals
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[2])
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

        # texture_buffer
        glBindTexture(GL_TEXTURE_2D, self.texture_buffer)

        # indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer[3])
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def update_buffers(self):

        # image
        glBindTexture(GL_TEXTURE_2D, self.texture_buffer)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_size[0], self.texture_size[1], 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, self.texture_data)

        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertex_coords)*4,
                     (ctypes.c_float * len(self.vertex_coords))(*self.vertex_coords),
                     GL_STATIC_DRAW)

        # texture
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.texture_coords)*4,
                     (ctypes.c_float * len(self.texture_coords))(*self.texture_coords)                     ,
                     GL_STATIC_DRAW)

        # normals
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[2])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.normal_coords)*4,
                     (ctypes.c_float * len(self.normal_coords))(*self.normal_coords),
                     GL_STATIC_DRAW)

        # indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.indices)*4,
                     (ctypes.c_uint * len(self.indices))(*self.indices),
                     GL_STATIC_DRAW)

    def draw(self):

        if self.shader is None:
            self.shader = Shader("../Interface/Shaders/vertex_shader.vs",
                                 "../Interface/Shaders/fragment_shader.fs")

            # matrices
            self.transform_model_view_loc = glGetUniformLocation(self.shader.program, 'transform_model_view_matrix')
            self.projection_loc = glGetUniformLocation(self.shader.program, 'projection_matrix')

        if self.buffer is None:
            self.create_vbo()

        if self.texture_buffer is None:
            self.create_texture()

        if self.update_awaiting:
            self.update_buffers()
            self.update_awaiting = False

        self.shader.begin()
        self.draw_vbo()
        self.shader.end()

    def read_model(self):
        pass

    def update_model_data(self, new_vertex_coord, new_texture_coord, new_texture_data, new_normal_coord, new_indices):

        self.vertices.extend(new_vertex_coord)
        self.texture_coords.extend(new_texture_coord)
        self.normal_coords.extend(new_normal_coord)
        self.texture_data.append(new_texture_data)
        new_index = len(self.indices)
        self.indices.extend([self.indices[new_index-2], self.indices[new_index-1], new_index])
        self.update_awaiting = True

    def save_scanned_room(self, room_name, vertex_coords, texture_coords, normal_coords, texture_data):

        try:

            # copy selected files to the new folder
            room_file = f'../res/Models/rooms/{room_name}/{room_name}.room'
            png_file = f'../res/Models/rooms/{room_name}/{room_name}.png'
            self.create_png_image(png_file, texture_data)
            self.create_room_file(room_file, vertex_coords, texture_coords, normal_coords)

        except IOError as e:
            print(e)

    @staticmethod
    def create_png_image(png_file, texture_data):
        height, width = 400, 400
        img = numpy.zeros((height, width, 4), numpy.uint8)

        for v in range(height):
            for u in range(width):
                if u+v*height < len(texture_data):
                    img[u][v] = x[u+v*height]
                else:
                    img[u][v] = (0, 0, 0, 255)

        cv2.imwrite(png_file, img)

    @staticmethod
    def create_room_file(room_file, vertex_coords, texture_coords, normal_coords):

        with open(room_file, 'w') as f:

            for index in range(0, len(vertex_coords), 3):
                f.write(" ".join(['v', *vertex_coords[index:index+3]]) + '\n')

            for index in range(0, len(texture_coords), 2):
                f.write(" ".join(['vt', *texture_coords[index:index+2]]) + '\n')

            for index in range(0, len(normal_coords), 3):
                f.write(" ".join(['vn', *normal_coords[index:index+3]]) + '\n')
