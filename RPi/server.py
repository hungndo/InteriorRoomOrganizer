import asyncio
import RPi.GPIO as GPIO
from Electronics.servo import Servo
from Electronics.lidar_lite import Lidar_Lite
from Electronics.camera import Camera
import time
import socket
import math

pitch_servo = Servo(11)
yaw_servo = Servo(13)
camera = Camera(resolution=(640, 480))


def scan():
    global yaw_servo, pitch_servo, camera

    camera.start_video_thread()

    lidar = Lidar_Lite()
    connected = lidar.connect(1)
    print("[start scanning]")

    pitch_servo.reset_pin()
    yaw_servo.reset_pin()
    pitch_servo.set_period(pitch_servo.current_period)
    yaw_servo.set_period(yaw_servo.current_period)

    if connected == 0:

        # start
        for pitch in range(0, 180, 2):

            for yaw in range(0, 180, 1):
                yaw_servo.turn(1)
                color = camera.get_pixel_color()
                data = f'{lidar.getDistance()} {color[0]} {color[1]} {color[2]}'
                yield data

            pitch_servo.turn(1)

            for yaw in range(180, 0, -1):
                yaw_servo.turn(-1)
                color = camera.get_pixel_color()
                data = f'{lidar.getDistance()} {color[0]} {color[1]} {color[2]}'
                yield data

            pitch_servo.turn(1)

        # reset periods for next use
        pitch_servo.reset()
        yaw_servo.reset()
        camera.stop()
        GPIO.cleanup()

        print("DONE!")

    else:
        return "Lidar not connected"


async def backend(reader, writer):
    # s = socket.socket()
    # s.bind(('', 1234))
    # s.listen(1)
    # client, addr = s.accept()

    is_scanning = await reader.read(1024)
    str_to_bool(is_scanning.decode('utf-8'))
    # await asyncio.sleep(0.00001)

    if is_scanning:
        count = 0
        for data in scan():
            # is_scanning = await reader.read(1024)
            # str_to_bool(is_scanning.decode('utf-8'))
            # if not is_scanning:
            #	pitch_servo.reset()
            #	yaw_servo.reset()
            ##	GPIO.cleanup()
            #	print("Hi")
            #	break

            split_data = data.split()
            distance = float(split_data[0])
            r, g, b = split_data[1], split_data[2], split_data[3]
            count += 1
            u = count % 400
            v = count // 400

            # print('Here '+ str(count)+ ' ' + str(distance))

            if distance % 10 > 5:
                distance = distance - distance % 10 + 10
            else:
                distance = distance - distance % 10

            # print(distance)

            if str(distance):

                x = distance * -math.cos(math.radians(yaw_servo.current_angle))
                y = distance * math.sin(math.radians(pitch_servo.current_angle))
                if pitch_servo.current_angle < 90:
                    z = -distance * math.sin(math.radians(yaw_servo.current_angle))
                else:
                    z = distance * math.sin(math.radians(yaw_servo.current_angle))

                x = format(x, '.8f')
                y = format(y, '.8f')
                z = format(z, '.8f')

                data = f'{x}/{y}/{z}' \
                    f'/{u}/{v}' \
                    f'/{r}/{g}/{b}/255 '

                # print(str(count) + ' ' + data)

                writer.write(data.encode('utf-8'))
                await writer.drain()
            # await asyncio.sleep(0.00001)

        # send to stop the while loop in client
        writer.write(b'False')
    # await writer.drain()

    # client.close()
    # s.shutdown(socket.SHUT_RDWR)
    # s.close()


def str_to_bool(string):
    if string == 'True':
        return True

    elif string == 'False':
        return False

    else:
        raise ValueError(f'Cannot convert {string} to bool')


if __name__ == '__main__':

    try:
        loop = asyncio.get_event_loop()
        server = asyncio.start_server(backend, '', 1234, loop=loop)
        # server = websockets.serve(backend,'192.168.137.175', 1234)

        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt as e:
        print('Keyboard Interrupt')
        camera.stop()
        GPIO.cleanup()
    except ValueError as e:
        print(e)
    except ConnectionError as e:
        GPIO.cleanup()
        print(e)
