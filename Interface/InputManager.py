from OpenGL.GLUT import *


class InputManager:

    def __init__(self, x, y, room, object_list, camera):

        self.room = room
        self.object_list = object_list
        self.camera = camera

        self.OFFSET_TO_CHANGE_ANGLE = 100
        self.CANVAS_DIMENSIONS = (x, y)

    def keyboard(self, *args):

        key = chr(args[0].GetKeyCode())
        if key == 'A':
            self.camera.move_left()
        if key == 'D':
            self.camera.move_right()
        if key == 'W':
            self.camera.move_inward()
        if key == 'S':
            self.camera.move_outward()

        if key == 'U':
            self.object_list.move_up(1)
        if key == 'O':
            self.object_list.move_down(1)
        if key == 'J':
            self.object_list.move_left(1)
        if key == 'L':
            self.object_list.move_right(1)
        if key == 'I':
            self.object_list.move_inward(1)
        if key == 'K':
            self.object_list.move_outward(1)
        if key == 'M':
            self.object_list.yaw_left()
        if key == ',':
            self.object_list.yaw_right()


    def keyboard_up(self, *args):

        key = chr(args[0].GetKeyCode())

        if key == 'A' or key == 'D':
            self.camera.stop_moving_in_x_direction()
        if key == 'W' or key == 'S':
            self.camera.stop_moving_in_z_direction()

        if key == 'U' or key == 'O':
            self.object_list.stop_moving_in_y_direction()
        if key == 'J' or key == 'L':
            self.object_list.stop_moving_in_x_direction()
        if key == 'I' or key == 'K':
            self.object_list.stop_moving_in_z_direction()
        if key == 'M' or key == ',':
            self.object_list.stop_yawing()

    def mouse_passive_motion(self, *args):

        mouse_position = args[0].GetPosition()
        # rotate left
        if mouse_position[0] < self.OFFSET_TO_CHANGE_ANGLE:
            self.camera.yaw_left()
        # rotate right
        elif self.CANVAS_DIMENSIONS[0] - 5 > mouse_position[0] > self.CANVAS_DIMENSIONS[0]-self.OFFSET_TO_CHANGE_ANGLE:
            self.camera.yaw_right()
        else:
            self.camera.stop_yawing()
