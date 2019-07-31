import asyncio
from Interface.MyApp import MyApp
import socket

app = MyApp()


async def message():

    while True:

        is_scanning = await app.is_scanning()
        if is_scanning == 'True':

            # set up client and connect to server
            # TODO: fix the error when trying to scan the second time
            reader, writer = await asyncio.open_connection('192.168.137.2', 1234)
            writer.write(b'True')
            # await writer.drain()

            # collect data
            count = 0
            while is_scanning == 'True':

                try:

                    data_list = await reader.read(2024)
                    data_list = data_list.decode('utf-8').split()

                    for data in data_list:
                        count += 1
                        # print('Here ' + str(count))

                        if data != 'False':
                            data = data.split('/')
                            if len(data) == 9:

                                # TODO handle missing data
                                data_is_missing = False
                                for i in range(len(data)):
                                    if data[i] == '':
                                        data_is_missing = True
                                        break
                                if data_is_missing:
                                    continue

                                        # print('missing')
                                        # data[i] = '0'
                                print(str(count) +' ' + str(data))

                                app.update_data((float(data[0]), float(data[1]), float(data[2])),    # vertex_coord
                                                (int(data[3]), int(data[4])),             # texture_coord
                                                (int(data[5]), int(data[6]), int(data[7]), int(data[8])),    # texture_data
                                                (0, 0, 0)                       # normal_coord
                                                )
                            is_scanning = await app.is_scanning()
                            if not is_scanning:
                                break
                        else:
                            is_scanning = data
                            print('DONE SCANNING')
                            break

                except ConnectionError:

                    print('Reconnecting')
                    reader, writer = await asyncio.open_connection('192.168.137.2', 1234)
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
