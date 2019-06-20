from Interface.Model import Model
from Interface.Transform import Transform


class Furniture(Model, Transform):
    def __init__(self):

        Model.__init__(self)
        Transform.__init__(self)

        self.ROTATE_SPEED = 0.5

        size = 50.0
        self.vertices = [
            size, -size, -size,
            size, size, -size,
            -size, size, -size,
            -size, -size, -size,
            size, -size, size,
            size, size, size,
            -size, size, size,
            -size, -size, size
        ]

        self.colors = [
            0, 0, 0,
            1, 0, 0,
            0, 1, 0,
            1, 1, 0,
            0, 0, 1,
            1, 0, 1,
            0, 1, 1,
            1, 1, 1
        ]

        self.indices = [
            0, 1, 2, 2, 3, 0,
            0, 4, 5, 5, 1, 0,
            0, 3, 7, 7, 4, 0,
            6, 5, 1, 1, 2, 6,
            6, 2, 3, 3, 7, 6,
            6, 7, 4, 4, 5, 6
        ]

    def move_left(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_left()

    def move_right(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_right()

    def move_inward(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_inward()

    def move_outward(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_outward()

    def move_up(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_up()

    def move_down(self, moving_speed):
        self.moving_speed = moving_speed
        super().move_down()
