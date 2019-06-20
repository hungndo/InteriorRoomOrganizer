from Interface.Transform import *


class Camera(Transform):

    def __init__(self):

        Transform.__init__(self)

        self.moving_speed = -2.0
        self.ROTATE_SPEED = 0.1
