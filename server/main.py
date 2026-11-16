import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK

listOfGames: dict

async def handler(websocket):
    otherPlayer = None

    async for message in websocket:
        pieces = message.split();
        print(pieces)

    del openClients[str(websocket)]

async def main():
    server = await serve(handler, "localhost", 8001)
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
