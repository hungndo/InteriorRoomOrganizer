from OpenGL.GL import *
from Interface.Shader import Shader
import cv2


class Model:

    def __init__(self):

        self.vertex_coords = []
        self.texture_coords = []
        self.normal_coords = []
        self.indices = []

        self.image = None
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

        # # indices
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer[3])
        # glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_coords))

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

        # # indices
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer[3])
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER,
        #              len(self.indices)*4,
        #              (ctypes.c_uint * len(self.indices))(*self.indices),
        #              GL_STATIC_DRAW)

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

    def update_model_data(self, new_vertex_coord, new_texture_coord, new_texture_data, new_normal_coord):

        # the reason why i make two additional vertices for each collected is because I want to draw
        # a triangle for each

        # this may help avoiding dependencies wrong collected vertex that may skew the model

        # TODO further data cloud optimization algorithm is needed to improve the quality of the model

        deviation = 3 # this determines how far two additionally generated vertices vary from the collected one

        self.vertex_coords.extend(list(map(float, new_vertex_coord)))
        self.vertex_coords.extend(list(map(float, [new_vertex_coord[0] + deviation,
                                                   new_vertex_coord[1] + deviation,
                                                   new_vertex_coord[2] + deviation])))

        self.vertex_coords.extend(list(map(float, [new_vertex_coord[0] - deviation,
                                                   new_vertex_coord[1] + deviation,
                                                   new_vertex_coord[2] - deviation])))

        # u v
        vt = [float(new_texture_coord[0])/self.texture_size[0], float(new_texture_coord[1])/self.texture_size[1]]
        self.texture_coords.extend(vt)
        self.texture_coords.extend(vt)
        self.texture_coords.extend(vt)

        self.normal_coords.extend(list(map(float, new_normal_coord)))
        self.normal_coords.extend(list(map(float, new_normal_coord)))
        self.normal_coords.extend(list(map(float, new_normal_coord)))

        # only when processing with image uv array, we have to access it img[v][u]
        self.image[new_texture_coord[1], new_texture_coord[0]] = list(map(int, new_texture_data))
        self.texture_data[new_texture_coord[0] + self.texture_size[1]*new_texture_coord[1]] = \
            self.image[new_texture_coord[1], new_texture_coord[0]]
        # # print(self.indices)
        # new_index = int(len(self.vertex_coords)/3) - 1
        # if new_index < 3:
        #     self.indices.append(new_index)
        # else:
        #     self.indices.extend((new_index-2, new_index-1, new_index))
        #
        self.update_awaiting = True

    @staticmethod
    def create_png_image( png_file, img):

        # since opencv reads images in BGRA mode,we need to convert the texture_data to BGRA

        texture_data = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(png_file, texture_data)

    @staticmethod
    def create_room_file(room_file, vertex_coords, texture_coords, normal_coords):

        with open(room_file, 'w') as f:

            for index in range(0, len(vertex_coords), 3):
                f.write(" ".join(['v', *list(map(str, vertex_coords[index:index+3]))]) + '\n')

            for index in range(0, len(texture_coords), 2):
                f.write(" ".join(['vt', *list(map(str,texture_coords[index:index+2]))]) + '\n')

            for index in range(0, len(normal_coords), 3):
                f.write(" ".join(['vn', *list(map(str,normal_coords[index:index+3]))]) + '\n')

    def __delete__(self, instance):
        glDeleteBuffers(4, self.buffer)
        glDeleteBuffers(1, self.texture_buffer)
