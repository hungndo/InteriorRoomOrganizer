import wx
from wx.glcanvas import GLCanvas, GLContext
from OpenGL.GL import *
from OpenGL.GLU import *
from Interface.Furniture import Furniture
from Interface.InputManager import InputManager
from Interface.Camera import *
from Interface.Room import Room


class MyCanvas(GLCanvas):

    def __init__(self, parent):
        GLCanvas.__init__(self, parent, -1, size=(850, 700), pos=(0, 0))

        # init context
        self.init = False
        self.context = GLContext(self)
        self.SetCurrent(self.context)

        # init objects
        self.room = Room("..\\res\\Models\\rooms\\3.room")
        self.furniture = Furniture()
        self.camera = Camera()
        self.input = InputManager(850, 700, self.room, self.furniture, self.camera)

        # init canvas
        glClearColor(0.0, 0.0, 0.0, 0.0)
        # glClearDepth(1)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.resize(None)

        # bind function
        self.Bind(wx.EVT_SIZE, self.resize)
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_KEY_DOWN, self.input.keyboard)
        self.Bind(wx.EVT_KEY_UP, self.input.keyboard_up)
        self.Bind(wx.EVT_MOTION, self.input.mouse_passive_motion)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def OnIdle(self, event):
        self.Refresh()

    def paint(self, event):
        self.display()

    def display(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0, -100.0)

        self.camera.update_position()
        self.furniture.update_position()

        # draw block in coordinate of the room
        glPushMatrix()
        glTranslatef(self.camera.xPosition, self.camera.yPosition, self.camera.zPosition)
        glRotatef(self.camera.yawSpinAngle, 0, True, 0)
        self.room.draw()

        glPushMatrix()
        glTranslatef(self.furniture.xPosition, self.furniture.yPosition, self.furniture.zPosition)
        glRotatef(self.furniture.yawSpinAngle, 0, True, 0)

        self.furniture.draw()

        glPopMatrix()
        glPopMatrix()

        self.SwapBuffers()

    def resize(self, event):

        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(size.width)/float(size.height), 0.1, 4000.0)
