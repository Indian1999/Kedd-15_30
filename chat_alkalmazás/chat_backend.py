import json
from fastapi import FastAPI, Websocket, WebSocketDisconnect
import time

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Websocket] = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                await self.disconnect(connection)

manager = ConnectionManager()
message_history = []

@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await manager.connect(websocket)
    await websocket.send_text(json.dumps(message_history))

    try:
        while True:
            data = await websocket.recieve_text()
            try:
                payload = json.loads(data)
                username = payload.get("username")
                text = payload.get("text")
                if not username or not text:
                    continue
            except:
                continue

            msg = {
                "username": username,
                "text": text,
                "timestamp": time.time()
            }

            message_history.append(msg)
            await manager.broadcast(msg)
    except:
        await manager.disconnect(websocket)
        
