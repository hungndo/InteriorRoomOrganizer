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

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    group = asyncio.gather(app.MainLoop())#,message())

    loop.run_until_complete(group)
    loop.run_forever()
    loop.close()
