from OpenGL.GL import *
from Interface.Shader import Shader


class Model():

    def __init__(self):

        self.vertices = []
        self.colors = []
        self.indices = []
        self.shader = None
        self.buffer = None

    def create_vbo(self):

        buffers = glGenBuffers(3)

        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertices)*4,
                     (ctypes.c_float * len(self.vertices))(*self.vertices),
                     GL_STATIC_DRAW)

        # colors
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.colors)*4,
                     (ctypes.c_float * len(self.colors))(*self.colors),
                     GL_STATIC_DRAW)

        # indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.indices)*4,
                     (ctypes.c_uint * len(self.indices))(*self.indices),
                     GL_STATIC_DRAW)

        return buffers

    def draw_vbo(self):

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glVertexPointer(3, GL_FLOAT, 0, None)

        # colors
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        glColorPointer(3, GL_FLOAT, 0, None)

        # indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer[2])
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

    def draw(self):

        if self.shader is None:

            self.shader = Shader(
                '''
                void main()
                {
                    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    gl_FrontColor = gl_Color;
                }
            ''',
                '''
                void main()
                {
                    gl_FragColor = gl_Color;
                }
            '''
            )

        if self.buffer is None:
            self.buffer = self.create_vbo()

        self.shader.begin()
        self.draw_vbo()
        self.shader.end()

    # def grouping_dots(self):
    #     print("group")
    #
    # def FindSurface(self):
    #     print("surface")
    #
    # def FindCorner(self):
    #     print("corner")


