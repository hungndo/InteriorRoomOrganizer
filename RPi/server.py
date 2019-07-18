import asyncio
import websockets
import RPi.GPIO as GPIO
from Electronics.servo import Servo
from Electronics.lidar_lite import Lidar_Lite
import time
import socket

pitch_servo = Servo(11)
yaw_servo = Servo(13)


def scan():
    global yaw_servo, pitch_servo

    lidar = Lidar_Lite()
    connected = lidar.connect(1)
    print("io")

    pitch_servo.set_period(pitch_servo.current_period)
    yaw_servo.set_period(yaw_servo.current_period)

    if connected == 0:

        # start
        for pitch in range(0, 180, 2):

            for yaw in range(180):
                yaw_servo.turn(1)
                yield lidar.getDistance()

            pitch_servo.turn(1)

            for yaw in range(180, 0, -1):
                yaw_servo.turn(-1)
                yield lidar.getDistance()

            pitch_servo.turn(1)

        # reset periods for next use
        pitch_servo.reset()
        yaw_servo.reset()

        GPIO.cleanup()
        print("DONE!")

    else:
        return "Lidar not connected"


async def backend():
    s = socket.socket()
    s.bind(('', 1234))
    s.listen(1)
    client, addr = s.accept()

    is_scanning = client.recv(1024).decode('utf-8')
    str_to_bool(is_scanning)
    await asyncio.sleep(0.00001)

    if is_scanning:
        count = 0
        for distance in scan():
            count += 1
            print('Here ' + str(count) + ' ' + str(distance))

            if str(distance):
                data = f'd{str(distance)} '
                client.send(data.encode('utf-8'))
                await asyncio.sleep(0.00001)

        # send to stop the while loop in client
        client.send(b'False')
        client.close()
        s.shutdown(socket.SHUT_RDWR)
        s.close()


def str_to_bool(string):
    if string == 'True':
        return True

    elif string == 'False':
        return False

    else:
        raise ValueError(f'Cannot convert {string} to bool')


if __name__ == '__main__':

    try:
        # start_server = websockets.serve(backend,'192.168.137.175', 1234)
        asyncio.get_event_loop().run_until_complete(backend())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt as e:
        print('Keyboard Interrupt')
        GPIO.cleanup()
    except ValueError as e:
        print(e)
    except ConnectionError as e:
        GPIO.cleanup()
        print(e)
