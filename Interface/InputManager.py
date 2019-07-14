from OpenGL.GLUT import *


class InputManager:

    def __init__(self, x, y, room, object_dict, camera):

        self.room = room
        self.object_dict = object_dict
        self.camera = camera

        self.OFFSET_TO_CHANGE_ANGLE = 100
        self.OFFSET_TO_STOP_CHANGING_ANGLE = 30
        self.CANVAS_DIMENSIONS = (x, y)

        # if there is no obj in obj_dict, there is no current moving obj
        # if there is one or more obj, the current moving obj is the first one
        self.current_obj_key = None

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

        if not self.current_obj_key is None:

            if key == 'U':
                self.object_dict[self.current_obj_key].move_up(1)
            if key == 'O':
                self.object_dict[self.current_obj_key].move_down(1)
            if key == 'J':
                self.object_dict[self.current_obj_key].move_left(1)
            if key == 'L':
                self.object_dict[self.current_obj_key].move_right(1)
            if key == 'I':
                self.object_dict[self.current_obj_key].move_inward(1)
            if key == 'K':
                self.object_dict[self.current_obj_key].move_outward(1)
            if key == 'M':
                self.object_dict[self.current_obj_key].yaw_left()
            if key == ',':
                self.object_dict[self.current_obj_key].yaw_right()

    def keyboard_up(self, *args):

        key = chr(args[0].GetKeyCode())

        if key == 'A' or key == 'D':
            self.camera.stop_moving_in_x_direction()
        if key == 'W' or key == 'S':
            self.camera.stop_moving_in_z_direction()

        # if there is object to move
        if not self.current_obj_key is None:

            if key == 'U' or key == 'O':
                self.object_dict[self.current_obj_key].stop_moving_in_y_direction()
            if key == 'J' or key == 'L':
                self.object_dict[self.current_obj_key].stop_moving_in_x_direction()
            if key == 'I' or key == 'K':
                self.object_dict[self.current_obj_key].stop_moving_in_z_direction()
            if key == 'M' or key == ',':
                self.object_dict[self.current_obj_key].stop_yawing()

    def mouse_passive_motion(self, *args):

        mouse_position = args[0].GetPosition()
        # rotate left
        if self.OFFSET_TO_STOP_CHANGING_ANGLE < mouse_position[0] < self.OFFSET_TO_CHANGE_ANGLE:
            self.camera.yaw_left()
        # rotate right
        elif self.CANVAS_DIMENSIONS[0] - self.OFFSET_TO_STOP_CHANGING_ANGLE > mouse_position[0] \
                > self.CANVAS_DIMENSIONS[0]-self.OFFSET_TO_CHANGE_ANGLE:
            self.camera.yaw_right()
        else:
            self.camera.stop_yawing()

    def set_current_moving_object(self, object_key):

        if object_key == 'Nothing':
            self.current_obj_key = None
        else:
            self.current_obj_key = object_key
