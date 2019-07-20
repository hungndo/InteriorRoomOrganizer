
class Transform:

    def __init__(self):

        self.moving_speed = 0
        self.ROTATE_SPEED = 0

        self.xVel = 0.0
        self.yVel = 0.0
        self.zVel = 0.0
        self.pitch_rotate_speed = 0.0
        self.yaw_rotate_speed = 0.0
        self.roll_rotate_speed = 0.0

        self.xPosition = 0.0
        self.yPosition = 0.0
        self.zPosition = 0.0
        self.pitchSpinAngle = 0.0
        self.yawSpinAngle = 0.0
        self.rollSpinAngle = 0.0

        self.scale = 1.0

    def move_left(self):
        self.xVel = -self.moving_speed

    def move_right(self):
        self.xVel = self.moving_speed

    def move_inward(self):
        self.zVel = -self.moving_speed

    def move_outward(self):
        self.zVel = self.moving_speed

    def move_up(self):
        self.yVel = self.moving_speed

    def move_down(self):
        self.yVel = -self.moving_speed

    def yaw_left(self):
        self.yaw_rotate_speed = -self.ROTATE_SPEED

    def yaw_right(self):
        self.yaw_rotate_speed = self.ROTATE_SPEED

    def stop_moving_in_x_direction(self):
        self.xVel = 0

    def stop_moving_in_z_direction(self):
        self.zVel = 0

    def stop_moving_in_y_direction(self):
        self.yVel = 0

    def stop_yawing(self):
        self.yaw_rotate_speed = 0

    def scale_model(self, scale_speed):
        self.scale += scale_speed

    def update_position(self):

        self.xPosition += self.xVel
        self.yPosition += self.yVel
        self.zPosition += self.zVel
        self.pitchSpinAngle += self.pitch_rotate_speed
        self.yawSpinAngle += self.yaw_rotate_speed
        self.rollSpinAngle += self.roll_rotate_speed
