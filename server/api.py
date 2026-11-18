from typing import Any
#from clientUtils import ClientData

from websockets.asyncio.server import ServerConnection

from gameClasses import Game

class Room:
    def __init__(self, password: str, hostSocket: ServerConnection):
        self.password: str = password
        self.hostClient: ServerConnection = hostSocket
        self.guestClients: list[ServerConnection] = []
        self.playerOne: ServerConnection = None
        self.playerTwo: ServerConnection = None
        self.game = Game()
    
    def setPlayerOne(self, client):
        if client != self.hostClient and client not in self.guestClients:
            return False
        else:
            self.playerOne = client

    def setPlayerTwo(self, client):
        if client != self.hostClient and client not in self.guestClients:
            return False
        else:
            self.playerTwo = client

    def addGuest(self, guest: ServerConnection):
        self.guestClients.append(guest)

    def sendGameDataToPlayerOne():
        pass

    def sendGameDataToPlayerTwo():
        pass

    def sendGameDataToAllSpectator():
        pass

    def sendGameDataToAllClients():
        pass

    def sendRoomCloseToGuests():
        pass

activeRooms: dict[str, Room] = {}

def roomIsAvailible(roomName: str):
    return str not in activeRooms.keys()
    
def createRoom(roomName: str, roomPassword: str, hostingSocket: ServerConnection):
    if roomIsAvailible(roomName):
        activeRooms[roomName] = Room(roomPassword, hostingSocket)
        return roomName
    else:
        return ""

def joinRoom(roomName: str, roomPassword: str, hostingSocket: ServerConnection):
    if roomName in activeRooms.keys():
        activeRooms[roomName].addGuest()
    else:
        pass

def closeRoom(roomName: str):
    activeRooms[roomName].sendRoomCloseToGuests()
    del activeRooms[roomName]