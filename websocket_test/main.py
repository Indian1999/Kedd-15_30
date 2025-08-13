from fastapi import FastAPI, WebSocket

app = FastAPI()
class valami():
    def __init__(self):
        pass
    async def connect(self, websocket):
        await websocket.accept()

manager = valami()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    #await websocket.accept()
    await websocket.send_text("Hello WebSocket")
    await websocket.close()
