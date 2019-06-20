import asyncio
import websockets


async def response(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"We got a message from the client: {message}")
        #await websocket.send("I can confirm I got your message!")

start_server = websockets.serve(response, '192.168.137.1', 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
