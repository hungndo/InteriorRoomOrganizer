import RPi.GPIO as GPIO
import time

hservo = 13
vservo = 11

PITCH_MIN_DUTY_CYCLE = 2.55
YAW_MIN_DUTY_CYCLE = 2.57
PITCH_MAX_DUTY_CYCLE = 11.8
YAW_MAX_DUTY_CYCLE = 11.9

PERIOD_PER_PITCH_ANGLE = (PITCH_MAX_DUTY_CYCLE - PITCH_MIN_DUTY_CYCLE) / 180
PERIOD_PER_YAW_ANGLE = (YAW_MAX_DUTY_CYCLE - YAW_MIN_DUTY_CYCLE) / 180

pitch_period = PITCH_MIN_DUTY_CYCLE
yaw_period = YAW_MIN_DUTY_CYCLE

GPIO.setmode(GPIO.BOARD)

GPIO.setup(vservo, GPIO.OUT)
pitch = GPIO.PWM(vservo, 50)

GPIO.setup(hservo, GPIO.OUT)
yaw = GPIO.PWM(hservo, 50)

pitch_angle = 0
yaw_angle = 0

def reset():

	pitch.start(PITCH_MIN_DUTY_CYCLE)
	yaw.start(YAW_MIN_DUTY_CYCLE)
	time.sleep(1)


def turn_pitch(counterclockwise, delta):
    # counterclockwise can only have value 1, -1
    # 1 = up, -1 = down

    global pitch_period, pitch

    if (pitch_period + counterclockwise * delta) > PITCH_MAX_DUTY_CYCLE:

        pitch_period = PITCH_MAX_DUTY_CYCLE
        pitch.ChangeDutyCycle(pitch_period)

    elif (pitch_period + counterclockwise * delta) < PITCH_MIN_DUTY_CYCLE:

        pitch_period = PITCH_MIN_DUTY_CYCLE
        pitch.ChangeDutyCycle(pitch_period)

    else:

        pitch_period += counterclockwise * delta
        pitch.ChangeDutyCycle(pitch_period)

    time.sleep(0.005)
    #print("PITCH: " + str(pitch_period) + " " + str((pitch_period - PITCH_MIN_DUTY_CYCLE) / PERIOD_PER_PITCH_ANGLE))


def turn_yaw(counterclockwise, delta):
    # counterclockwise can only have value 1, -1
    # 1 = counterclockwise, -1 = clockwise

    global yaw_period, yaw

    if (yaw_period + (-counterclockwise * delta)) > YAW_MAX_DUTY_CYCLE:

        yaw_period = YAW_MAX_DUTY_CYCLE
        yaw.ChangeDutyCycle(yaw_period)

    elif (yaw_period + (-counterclockwise * delta)) < YAW_MIN_DUTY_CYCLE:

        yaw_period = YAW_MIN_DUTY_CYCLE
        yaw.ChangeDutyCycle(yaw_period)

    else:

        yaw_period += -counterclockwise * delta
        yaw.ChangeDutyCycle(yaw_period)

    time.sleep(0.005)
    #print("YAW: " + str(yaw_period) + " " + str((yaw_period - YAW_MIN_DUTY_CYCLE) / PERIOD_PER_YAW_ANGLE))
