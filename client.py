import asyncio
import pickle

import websockets

from downloader import download


async def listen():
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url) as ws:
        await ws.send('Hello Server!')

        while True:
            raw_data = await ws.recv()

            data = pickle.loads(raw_data)
            print(f'Data from server: {data}')

            print('Start downloading!')

            for url in data:
                if not url['processed']:
                    download(link=url['url'], size_in_bytes=url['size'], threads=5, bytes_limit=30000)

            print('Stop downloading!')


asyncio.get_event_loop().run_until_complete(listen())
