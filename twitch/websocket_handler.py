"""
From tutorial at https://websockets.readthedocs.io/en/stable/
"""

import asyncio
from websockets.asyncio.server import serve

class Websocket_Handler:

    def __init__(self, hostname="localhost", port=8080):
        self.hostname = hostname
        self.port = port

    async def serve(self, task):
        async with serve(task, self.hostname, self,port) as server:
            await server.serve_forever()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
