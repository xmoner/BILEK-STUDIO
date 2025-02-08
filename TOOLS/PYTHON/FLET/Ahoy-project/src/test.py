import websockets
import asyncio
from websockets.server import serve

async def handler(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())