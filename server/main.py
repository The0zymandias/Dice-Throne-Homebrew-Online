from websockets.asyncio.server import Server
from typing import Any
import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK

from gameInstance import gameInstance

from json import dumps, loads, JSONDecodeError

listOfGames: dict[str, gameInstance] = {}

async def handler(websocket) -> None:
    async for message in websocket:
        print(f"From sock {websocket.id}: {message}")
        try: 
            msgJson = loads(message)
        except JSONDecodeError as e:
            print(f"ERROR: {e.msg}")
        else:
            command = msgJson["command"]
            data = msgJson["data"]

async def main() -> None:
    server: Server = await serve(handler, "localhost", 8765)
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
