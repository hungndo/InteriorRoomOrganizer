import asyncio
import websockets
from Interface.MyApp import MyApp

app = MyApp()


async def message():

    while True:

        is_scanning = await app.is_scanning()
        if is_scanning == 'True':

            async with websockets.connect("ws://192.168.137.60:1234") as socket:

                # activate the loop in server
                await socket.send('True')

                # collect data
                while is_scanning == 'True':

                    try:
                        tmp = await socket.recv()
                        if tmp != 'False':
                            # do stuffs in here
                            print(await socket.recv())

                        else:
                            is_scanning = tmp
                            break
                    except:

                        break
                        # print('Reconnecting')
                        # socket = await websockets.connect("ws://192.168.137.60:1234")
                        # print(socket)

# async def start_scanning():
#     #
#     # if main_interface.app.frame.panel.is_scanning == 'False':
#     #     print("here")
#     #     # await websockets.send()
#     #     # main_interface.app.frame.panel.stop_scanning()
#     await asyncio.sleep(1)
#     print("hi")

# server = None


# async def start_server():
#     global server
#     server = websockets.serve(response, '192.168.137.1', 1234)
#     # asyncio.get_event_loop().run_until_complete(server)
#     # asyncio.get_event_loop().run_forever()
#

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    group = asyncio.gather(message(), app.MainLoop())

    loop.run_until_complete(group)
    loop.run_forever()
    loop.close()
