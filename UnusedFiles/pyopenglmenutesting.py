from OpenGL.GLUT import *
from OpenGL.GL import *
window = None
menu_id = None
submenu_id = None
value = None


def process_menu_events(num):
    if num == 0:
        glutDestroyWindow(window)

    else:
        global value
        value = num

    glutPostRedisplay()


def createMenu():

    submenu_id = glutCreateMenu(process_menu_events)
    glutAddMenuEntry("Sphere", 2)
    glutAddMenuEntry("Cone",3)
    glutAddMenuEntry("Torus", 4)
    glutAddMenuEntry("Sphere", 5)
    menu_id = glutCreateMenu(process_menu_events)
    glutAddMenuEntry("Clear", 1)
    print(submenu_id)
    glutAddSubMenu("Draw", submenu_id)
    glutAddMenuEntry("Quit", 0)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    return 0


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if value == 1:
        return
    elif value == 2:
        glPushMatrix()
        glColor3d(1.0,0.0, 0.0)
        print("something")
        glutWireSphere(0.5, 50, 50)
        glPopMatrix()
    elif value == 3:
        glPushMatrix()
        glColor3d(0.0,1.0,0.0)
        glRotated(65, -1.0, 0.0,0.0)
        glutWireCone(0.5,50,50)
        glPopMatrix()
    elif value == 4:
        glPushMatrix()
        glColor3d(0.0,0.0,1.0)
        glutWireTorus(0.3,0.6,100,100)
        glPopMatrix()
    elif value == 5:
        glPushMatrix()
        glColor3d(1.0,0.0,1.0)
        glutSolidTeapot(0.5)
        glPopMatrix()
    glFlush()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
    glutInitWindowSize(500,500)
    glutInitWindowPosition(100,100)
    window = glutCreateWindow(b"Test Menu")

    createMenu()
    glClearColor(0.0,0.0,0.0,0.0)

    glutDisplayFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    main()
