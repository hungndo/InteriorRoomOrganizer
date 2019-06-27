import asyncio
import websockets
import RPi.GPIO as GPIO
from Electronics import servo
from Electronics.lidar_lite import Lidar_Lite


def scan():
    lidar = Lidar_Lite()
    connected = lidar.connect(1)
    print("io")

    if connected == 0:

        # start
        for pitch in range(0, 180, 2):

            for yaw in range(180):
                servo.turn_yaw(-1, servo.PERIOD_PER_YAW_ANGLE)
                yield lidar.getDistance()

            servo.turn_pitch(1, servo.PERIOD_PER_PITCH_ANGLE)

            for yaw in range(180, 0, -1):
                servo.turn_yaw(1, servo.PERIOD_PER_YAW_ANGLE)
                yield lidar.getDistance()

            servo.turn_pitch(1, servo.PERIOD_PER_PITCH_ANGLE)

        GPIO.cleanup()
        print("DONE!")

    else:
        return "Lidar not connected"


async def backend(websocket, path):
    while True:

        start_scanning = await websocket.recv()

        if start_scanning == 'True':
            # reset
            servo.reset()
            for distance in scan():
                await websocket.send(str(distance))

            # send to stop the while loop in client
            await websocket.send('False')
            break


if __name__ == '__main__':
    start_server = websockets.serve(backend, '192.168.137.60', 1234)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
