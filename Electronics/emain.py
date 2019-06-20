import RPi.GPIO as GPIO
import servo


def scan():
    servo.yaw.ChangeDutyCycle(servo.YAW_MIN_DUTY_CYCLE)
    servo.pitch.ChangeDutyCycle(servo.PITCH_MIN_DUTY_CYCLE)

    for pitch in range(0, 180, 2):

        for yaw in range(180):
            servo.turn_yaw(-1, servo.PERIOD_PER_YAW_ANGLE)

        servo.turn_pitch(1, servo.PERIOD_PER_PITCH_ANGLE)

        for yaw in range(180, 0, -1):
            servo.turn_yaw(1, servo.PERIOD_PER_YAW_ANGLE)

        servo.turn_pitch(1, servo.PERIOD_PER_PITCH_ANGLE)

    GPIO.cleanup()
    print("DONE!")

scan()