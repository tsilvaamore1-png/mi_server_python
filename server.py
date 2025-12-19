import asyncio
import websockets
import json
import uuid

players = {}

async def handler(ws):
    pid = str(uuid.uuid4())
    players[pid] = {"x":0,"y":2,"z":0}

    await ws.send(json.dumps({"id":pid,"players":players}))

    try:
        async for msg in ws:
            data = json.loads(msg)

            if data["type"] == "pos":
                players[pid] = data["pos"]

                for socket in websockets.server.WebSocketServerProtocol.instances:
                    try:
                        await socket.send(json.dumps({"players":players}))
                    except:
                        pass

    except:
        pass
    
    del players[pid]

async def main():
    print("Servidor iniciado en puerto 8765")
    async with websockets.serve(handler, "", 8765):
        await asyncio.Future()

asyncio.run(main())
