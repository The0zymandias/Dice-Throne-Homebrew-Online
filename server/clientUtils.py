from json import dumps, loads, JSONDecodeError

def parseWebsocketJson(message):
    try: 
        msgJson = loads(message)
    except JSONDecodeError as e:
        return "", "", False
    else:
        return msgJson["cmd"], msgJson["data"], True