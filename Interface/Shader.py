from OpenGL.GL import *


class Shader(object):

    def __init__(self, vs_source, fs_source):
        # create program
        self.program = glCreateProgram()

        # create vertex shader
        self.vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vs, [vs_source])
        glCompileShader(self.vs)
        glAttachShader(self.program, self.vs)

        # create fragment shader
        self.fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fs, [fs_source])
        glCompileShader(self.fs)
        glAttachShader(self.program, self.fs)

        # link
        glLinkProgram(self.program)

    def begin(self):
        if glUseProgram(self.program):
            print("error")

    def end(self):
        glUseProgram(0)

