import asyncio
from Interface.MyApp import MyApp
import socket

app = MyApp()


async def message():

    while True:

        is_scanning = await app.is_scanning()
        if is_scanning == 'True':

            # set up client and connect to server
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect(('192.168.137.175', 1234))
            # s.send(b'True')
            # await asyncio.sleep(0.00001)
            reader, writer = await asyncio.open_connection('192.168.137.175', 1234)
            writer.write(b'True')
            # await writer.drain()
            # collect data
            count = 0
            while is_scanning == 'True':

                try:

                    data_list = await reader.read(2024)
                    data_list = data_list.decode('utf-8').split()
                    # await asyncio.sleep(0.00001)

                    for data in data_list:
                        # count += 1
                        # print('Here ' + str(count))

                        if data != 'False':
                            data = data.split('/')
                            if len(data) == 9:

                                for i in range(len(data)):
                                    if data[i] == '':
                                        data[i] = '255'
                                # print(data)
                                app.update_data((int(data[0]), int(data[1]), int(data[2])),    # vertex_coord
                                                (int(data[3]), int(data[4])),             # texture_coord
                                                (int(data[5]), int(data[6]), int(data[7]), int(data[8])),    # texture_data
                                                (0, 0, 0)                       # normal_coord
                                                )

                        else:
                            is_scanning = data
                            print('DONE SCANNING')
                            break

                except ConnectionError:

                    print('Reconnecting')
                    reader, writer = await asyncio.open_connection('192.168.137.175', 1234)
                    writer.write(b'True')

            # finish scanning and save newly scanned room
            writer.close()
            app.finish_scanning()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    group = asyncio.gather(app.MainLoop(),message())

    loop.run_until_complete(group)
    loop.run_forever()
    loop.close()
