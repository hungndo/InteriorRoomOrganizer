from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Interface.Furniture import Furniture
from Interface.Room import Room
from Interface.InputManager import InputManager
from Interface.Camera import *

import time

WINDOW_DIMENSIONS = (1000, 700)
room = None
input_manager = None
chair = None
camera = None


def display():
    global input_manager, room, chair, camera
    print("Hi")
    x = glGetDoublev(GL_MODELVIEW_MATRIX)
    print(x)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0.0, -WINDOW_DIMENSIONS[1]/3, -2000)

    camera.update_position()
    chair.update_position()

    # # draw block in coordinate of the screen
    # glPushMatrix()
    # glTranslatef(camera.xPosition, camera.yPosition, camera.zPosition)
    #
    # glPushMatrix()
    # glTranslatef(chair.xPosition, chair.yPosition, chair.zPosition)
    #
    # # --------------------------
    #
    # glRotatef(camera.yawSpinAngle, 0, True, 0)
    # glRotatef(chair.yawSpinAngle, 0, True, 0)
    # chair.draw()
    # glPopMatrix()
    #
    # glRotatef(camera.yawSpinAngle, 0, True, 0)
    # room.draw()
    # glPopMatrix()

    # draw block in coordinate of the room
    glPushMatrix()
    glTranslatef(camera.xPosition, camera.yPosition, camera.zPosition)
    glRotatef(camera.yawSpinAngle, 0, True, 0)
    room.draw()

    glPushMatrix()
    glTranslatef(chair.xPosition, chair.yPosition, chair.zPosition)
    glRotatef(chair.yawSpinAngle, 0, True, 0)
    chair.draw()
    glPopMatrix()
    glPopMatrix()
    ############
    #room.draw()

    glFlush()
    glutSwapBuffers()


def my_idle_function():

    time.sleep(0.010)
    glutPostRedisplay()


def resize(width, height):

    # viewport
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 4000.0)


def initialize():
    global room, input_manager, chair, camera

    room = Room("..\\Models\\rooms\\3.txt")

    chair = Furniture()

    camera = Camera()
    input_manager = InputManager(*WINDOW_DIMENSIONS, room, chair, camera)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)


if __name__ == '__main__':

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
    glutInitWindowSize(*WINDOW_DIMENSIONS)
    glutInitWindowPosition(100, 0)
    glutCreateWindow(b"Interior Room Organizer")

    initialize()

    glutDisplayFunc(display)
    glutIdleFunc(my_idle_function)
    glutReshapeFunc(resize)

    glutKeyboardFunc(input_manager.keyboard)
    glutKeyboardUpFunc(input_manager.keyboard_up)
    glutMouseFunc(input_manager.mouse)
    glutMotionFunc(None)
    glutPassiveMotionFunc(input_manager.mouse_passive_motion)
    glutSpecialFunc(input_manager.special_func)
    glutSpecialUpFunc(input_manager.special_up_func)
    from Interface.Menu import Menu

    glutMainLoop()

