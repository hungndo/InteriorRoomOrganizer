from OpenGL.GL import *
from Interface.Shader import Shader
import numpy


class Model:

    def __init__(self):

        self.vertices = []
        self.textures = []
        self.normals = []
        self.indices = []

        self.texture_data = None
        self.texture_size = None

        self.shader = None
        self.buffer = None
        self.texture_buffer = None

        self.transform_model_view_loc = None
        self.projection_loc = None

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
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_size[0], self.texture_size[1], 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, self.texture_data)
        glEnable(GL_TEXTURE_2D)

    def create_vbo(self):

        self.vertices = numpy.array(self.vertices, dtype='float32')
        self.textures = numpy.array(self.textures, dtype='float32')
        self.normals = numpy.array(self.normals, dtype='float32')
        #self.indices = numpy.array(self.indices, dtype='uint8')

        buffers = glGenBuffers(4)

        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertices)*4,
                     self.vertices,
                     GL_STATIC_DRAW)

        # texture
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.textures)*4,
                     self.textures,
                     GL_STATIC_DRAW)

        # normals
        glBindBuffer(GL_ARRAY_BUFFER, buffers[2])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.normals)*4,
                     self.normals,
                     GL_STATIC_DRAW)

        # indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.indices)*4,
                     (ctypes.c_uint * len(self.indices))(*self.indices),
                     GL_STATIC_DRAW)

        return buffers

    def draw_vbo(self):

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

    def draw(self):

        if self.shader is None:
            self.shader = Shader("../Interface/Shaders/vertex_shader.vs",
                                 "../Interface/Shaders/fragment_shader.fs")

            # matrices
            self.transform_model_view_loc = glGetUniformLocation(self.shader.program, 'transform_model_view_matrix')
            self.projection_loc = glGetUniformLocation(self.shader.program, 'projection_matrix')

        if self.buffer is None:
            self.buffer = self.create_vbo()

        if self.texture_buffer is None:
            self.create_texture()

        self.shader.begin()

        transform_model_view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)

        glUniformMatrix4fv(self.transform_model_view_loc, 1, GL_FALSE, transform_model_view_matrix)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection_matrix)

        self.draw_vbo()
        self.shader.end()

    def read_model(self):
        print("implemented by subclass")
