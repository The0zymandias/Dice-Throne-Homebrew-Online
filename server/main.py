from api import roomIsAvailible
from server.api import closeRoom
from api import createRoom
from api import *
from websockets.asyncio.server import Server
from typing import Any
import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from gameClasses import Game
from clientUtils import parseWebsocketJson

from json import dumps

mapCmdsToFunctions: dict[str, Any] = {
    "CREATE_ROOM": createRoom,
    "JOIN_ROOM": joinRoom,
    "REQUEST_PLAYER_1": None,
    "REQUEST_PLAYER_2": None,
    "REQUEST_SPECTATE": None,
    "UPDATE_GAME_STATE": None,
    "CLOSE_ROOM": None
}

async def parseCmdFromSocket(message, socketId):
    command, data = parseWebsocketJson(message, socketId)
    if command == "":
        print(f"JSON decode error from {socketId}, skipping: {message}")
        return "", ""
    return command, data

async def sendCmdToSocket(socket, cmd):
    print(f"'{cmd["cmd"]}' to {socket.id}: {cmd}")
    await socket.send(dumps(cmd))

async def handleMessage(websocket, message, currentRoomName):
    command, data, success = parseWebsocketJson(message)
    # Error parsing JSON
    if not success:
        print(f"JSON decode error from {websocket.id}, skipping: {message}")
        return

    print(f"'{command}' from {websocket.id}: {message}")
    try:
        match command:

            case "PING": # Note that the python websocket manages keepalive pings by itself
                await sendCmdToSocket(websocket, {
                    "cmd": "PONG",
                    "data": {"text": "Pong is a 1972 sports video game developed and published by Atari, Inc. for arcades."}
                })

            case "CREATE_ROOM":
                if currentRoomName != "":
                    await sendCmdToSocket(websocket, {
                        "cmd": "CREATE_ROOM_ERROR",
                        "data": {"msg": f"You're already in room {currentRoomName}"}
                    })
                elif not roomIsAvailible(data["room_name"]):
                    await sendCmdToSocket(websocket, {
                        "cmd": "CREATE_ROOM_ERROR",
                        "data": {"msg": f"'{data["room_name"]}' already exists"}
                    })

                else:
                    currentRoomName = createRoom(data["ROOM_NAME"], data["ROOM_PASSWORD"], websocket)
                    await sendCmdToSocket(websocket, {"cmd": "CREATE_ROOM_SUCCESS", "data": {}})                 

            case _:
                await sendCmdToSocket(websocket, {
                    "cmd": "FAILED_MAKE_ROOM",
                    "data": {
                        "msg": "ROOM_NAME_ALREADY_EXISTS"
                        }
                    }
                )
    except Exception as e:
        await sendCmdToSocket(websocket, {
            "cmd": "SERVER_ERROR",
            "data": {
                "msg": "INTERNAL_SERVER_ERROR"
            }
        })

async def handler(websocket) -> None:
    currentRoomName = ""
    try: 
        async for message in websocket:
            await handleMessage(websocket, message, currentRoomName)
    except ConnectionClosedOK:
        pass
    except ConnectionClosedError:
        pass
    finally:
        closeRoom(currentRoomName)
    
async def main() -> None:
    server: Server = await serve(handler, "localhost", 8765, server_header="DICE")
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
