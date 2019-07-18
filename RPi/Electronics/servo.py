import RPi.GPIO as GPIO
import time


class Servo:

    def __init__(self, pin):

        self.pin = pin

        self.MIN_DUTY_CYCLE = 2.57
        self.MAX_DUTY_CYCLE = 11.8

        self.PERIOD_PER_ANGLE = (self.MAX_DUTY_CYCLE - self.MIN_DUTY_CYCLE) / 180

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pitch = GPIO.PWM(self.pin, 50)

        self.current_angle = 0
        self.current_period = self.MIN_DUTY_CYCLE

    def set_period(self, dc):

        self.pitch.start(dc)
        time.sleep(1)

    def turn(self, delta_angle):

        #	positive -> up , right
        #	negative -> down, left

        delta_period = delta_angle * self.PERIOD_PER_ANGLE

        if (self.current_period + delta_period) > self.MAX_DUTY_CYCLE:

            self.current_period = self.MAX_DUTY_CYCLE
            self.pitch.ChangeDutyCycle(self.current_period)

        elif (self.current_period + delta_period) < self.MIN_DUTY_CYCLE:

            self.current_period = self.MIN_DUTY_CYCLE
            self.pitch.ChangeDutyCycle(self.current_period)

        else:

            self.current_period += delta_period
            self.pitch.ChangeDutyCycle(self.current_period)

        time.sleep(0.005)

    def reset(self):
        self.current_period = self.MIN_DUTY_CYCLE
        self.current_angle = 0