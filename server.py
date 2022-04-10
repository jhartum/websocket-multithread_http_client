import asyncio
import pickle

import websockets
import websockets.exceptions

import config
from data import prepare_data

PORT = 7890


async def server(websocket):
    print("Client connected")

    try:
        async for message in websocket:
            print(f"Received message: {message}")

            data = prepare_data(config.urls)
            await websocket.send(pickle.dumps(data))
    except websockets.exceptions.ConnectionClosed:
        print('Client disconnected')


print(f'Server start on port - {PORT}')
start_server = websockets.serve(server, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
