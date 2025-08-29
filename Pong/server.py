import asyncio
import json
import math
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

WIDTH, HEIGHT = 800, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 80
BALL_RADIUS = 8
PADDLE_SPEED = 340
BALL_SPEED = 320
FPS = 60

LEFT_X = 40
RIGHT_X = WIDTH - 40 - PADDLE_WIDTH

class Player:
    def __init__(self, name: str, ws: WebSocket, side: str):
        self.name = name
        self.ws = ws
        self.side = side
        self.input_up = False
        self.input_down = False
        self.connected = True
        
class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: dict = {} # kulcs: oldal (side), érték: Player objektum
        self.spectators: list[WebSocket] = [] # websocketek listája
        self.task_loop = None
        self.state_lock = asyncio.Lock()
        self.reset_state()
        
    def reset_state(self):
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        angle = math.radians(30) # pi / 6 radián
        direction = 1 if int(time.time()) % 2 == 0 else -1
        self.ball_x_velocity = math.cos(angle) * direction * BALL_SPEED
        self.ball_y_velocity = math.sin(angle) * BALL_SPEED
        self.left_y = HEIGHT // 2 + PADDLE_HEIGHT // 2
        self.right_y = HEIGHT // 2 + PADDLE_HEIGHT // 2
        self.score_left = 0
        self.score_right = 0
        self.gameOn = True
        self.last_tick = time.perf_counter()       
    
    def is_full(self):
        return self.players.__len__() >= 2
    
    def sides_free(self):
        return [side for side in ["left", "right"] if side not in self.players.keys()]
    
    async def broadcast(self, payload: dict):
        msg = json.dumps(payload)
        connections = [player.ws for player in self.players.values()] + self.spectators
        to_remove = []
        for ws in connections:
            try:
                await ws.send_text(msg)
            except:
                to_remove.append(ws)
        for ws in to_remove:
            if ws in self.spectators:
                self.spectators.remove(ws)
            else:
                for side, player in self.players.items():
                    if player.ws == ws:
                        del self.players[side]
                        
rooms: dict = {} # kulcs: room_id, érték: Room objektum

def get_room(room_id: str):
    if room_id not in rooms.keys():
        rooms[room_id] = Room(room_id)
    return rooms[room_id]
        
async def game_loop(room: Room):
    delta_time = 1 / FPS
    while True:
        if len(room.players) == 0 and len(room.spectators) == 0:
            room.gameOn = False
            return
        now = time.perf_counter()
        dt = now - room.last_tick
        room.last_tick = now
        steps = max(1, int(round(dt / delta_time)))
        step_dt = dt / steps if steps > 0 else delta_time
        
        async with room.state_lock:
            for _ in range(steps):
                if "left" in room.players.keys():
                    player = room.players["left"]
                    up_velocity = -PADDLE_SPEED if player.input_up else 0
                    down_velocity = PADDLE_SPEED if player.input_down else 0
                    velocity = up_velocity + down_velocity
                    if room.left_y + velocity >= 0 and room.left_y + velocity + PADDLE_HEIGHT <= HEIGHT:
                        room.left_y += velocity
                if "right" in room.players.keys():
                    player = room.players["right"]
                    up_velocity = -PADDLE_SPEED if player.input_up else 0
                    down_velocity = PADDLE_SPEED if player.input_down else 0
                    velocity = up_velocity + down_velocity
                    if room.right_y + velocity >= 0 and room.right_y + velocity + PADDLE_HEIGHT <= HEIGHT:
                        room.right_y += velocity
                        
                room.ball_x += room.ball_x_velocity * step_dt
                room.ball_y += room.ball_y_velocity * step_dt
                
                if room.ball_y <= 0 or room.ball_y >= HEIGHT:
                    room.ball_y_velocity *= -1
                
                # Bal oldali visszapattanás
                if room.ball_x + BALL_RADIUS <= LEFT_X + PADDLE_WIDTH:
                    if room.left_y + 5 <= room.ball_y and room.left_y - PADDLE_HEIGHT - 5 >= room.ball_y:
                        room.ball_x_velocity *= -1
                # Jobb oldali visszapattanás
                if room.ball_x - BALL_RADIUS <= RIGHT_X:
                    if room.right_y + 5 <= room.ball_y and room.right_y - PADDLE_HEIGHT - 5 >= room.ball_y:
                        room.ball_x_velocity *= -1
                        
                someone_scored = False
                who_scored = None
                if room.ball_x < 0 - BALL_RADIUS * 2:
                    who_scored = "right"
                    room.score_right += 1
                    someone_scored = True
                if room.ball_x > HEIGHT:
                    who_scored = "left"
                    room.score_left += 1
                    someone_scored = True
                
                # reset after goal
                if someone_scored:
                    room.ball_x = WIDTH // 2
                    room.ball_y = HEIGHT // 2
                    angle = math.radians(30) # pi / 6 radián
                    direction = 1 if int(time.time()) % 2 == 0 else -1
                    room.ball_x_velocity = math.cos(angle) * direction * BALL_SPEED
                    room.ball_y_velocity = math.sin(angle) * BALL_SPEED
                    
            await room.broadcast({
                "type": "state",
                "width": WIDTH,
                "height": HEIGHT,
                "left_x": LEFT_X, "right_x": RIGHT_X, 
                "paddle_width": PADDLE_WIDTH, "paddle_height": PADDLE_HEIGHT,
                "left_y": room.left_y, "right_y": room.right_y,
                "ball_x": room.ball_x, "ball_y": room.ball_y,
                "ball_radius": BALL_RADIUS,
                "score_left": room.score_left, "score_right": room.score_right,
                "players": {side: p.name for side, p in room.players.items()}
            })
            
        await asyncio.sleep(max(0.0, delta_time - (time.perf_counter() - now)))    
            
@app.get("/")
def root():
    return {"OK": True, "msg": "Pong server is running."}

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port="8000", reload=False)
    