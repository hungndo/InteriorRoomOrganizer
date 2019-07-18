import asyncio
from Interface.MyApp import MyApp
import socket

app = MyApp()


async def message():

    while True:

        is_scanning = await app.is_scanning()
        if is_scanning == 'True':

            # set up client and connect to server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('192.168.137.175', 1234))
            s.send(b'True')
            await asyncio.sleep(0.00001)

            # collect data
            count = 0
            while is_scanning == 'True':

                try:

                    data_list = s.recv(1024).decode('utf-8').split()
                    await asyncio.sleep(0.00001)

                    for data in data_list:
                        count += 1
                        print('Here ' + str(count))

                        if data != 'False':

                                # data = data.split()
                                # app.update_data((data[0], data[1], data[2]),     # vertex_coord
                                #                 (data[3], data[4]),             # texture_coord
                                #                 (data[5], data[6], data[7]),    # texture_data
                                #                 (data[8], data[9], data[10])    # normal_coord
                                #                 )

                                print(data)
                        else:
                            is_scanning = data
                            print('DONE SCANNING')
                            break

                except ConnectionError:

                    print('Reconnecting')
                    s.connect(('192.168.137.175', 1234))
                    s.send(b'True')

            # finish scanning and save newly scanned room
            s.close()
            app.finish_scanning()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    group = asyncio.gather(app.MainLoop(),message())

    loop.run_until_complete(group)
    loop.run_forever()
    loop.close()
