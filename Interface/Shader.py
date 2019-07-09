from OpenGL.GL import *

class Shader(object):

    def __init__(self, vs_source, fs_source):
        # create program
        self.program = glCreateProgram()

        # create vertex shader
        self.vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vs, self.loadShader(vs_source))
        glCompileShader(self.vs)
        glAttachShader(self.program, self.vs)

        # create fragment shader
        self.fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fs, self.loadShader(fs_source))
        glCompileShader(self.fs)
        glAttachShader(self.program, self.fs)

        # link
        glLinkProgram(self.program)

    def loadShader(self, source):
        shader_source = ''
        with open(source, 'r') as file:
            shader_source = file.read()

        return str.encode(shader_source)

    def begin(self):
        if glUseProgram(self.program):
            print("error")

    def end(self):
        glUseProgram(0)

