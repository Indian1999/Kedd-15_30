import asyncio
import websockets
import pygame
import json
import sys
import os
import argparse

WIDTH, HEIGHT = 800, 400
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class GameClient:
    def __init__(self, url):
        self.url = url
        self.side = "spectator"
        self.name = "Player"
        
        self.state = {
                "type": "state",
                "width": WIDTH,
                "height": HEIGHT,
                "left_x": 40, "right_x": WIDTH - 52, 
                "paddle_width": 12, "paddle_height": 80,
                "left_y": HEIGHT//2 - 40, "right_y": HEIGHT//2 - 40,
                "ball_x": WIDTH // 2, "ball_y": HEIGHT // 2,
                "ball_radius": 8,
                "score_left": 0, "score_right": 0,
                "players": {}
            }
        
        self.input_up = False
        self.input_down = False
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Client")
        self.normal_font = pygame.font.SysFont("Arial", 28)
        self.large_font = pygame.font.SysFont("Arial", 56)
        self.ws = None
        self.running = True
        self.info_msg = ""
    
    async def recieve_loop(self):
        if self.ws == None:
            raise Exception("GameClient.ws value is None")
        try:
            async for msg in self.ws:
                try:
                    data = json.loads(msg)
                except:
                    continue
                msg_type = data.get("type")
                if msg_type == "assignment":
                    self.side = data.get("side")
                    self.name = data.get("name")
                elif msg_type == "state":
                    self.state.update(data)
                elif msg_type == "info":
                    self.info_msg = data.get("msg")   
        except:
            self.running = False
            
    async def send_input(self):
        if not self.ws:
            return
        payload = {
            "type": "input",
            "up": self.input_up,
            "down": self.input_down
        }
        try:
            await self.ws.send(json.dumps(payload))
        except Exception as ex:
            print(ex)
        
    async def mainloop(self):
        async with websockets.connect(self.url) as ws:
            self.ws = ws
            recieve_task = asyncio.create_task(self.recieve_loop())
            try:
                while self.running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.input_up = True
                            if event.key == pygame.K_DOWN:
                                self.input_down = True
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_UP:
                                self.input_up = False
                            if event.key == pygame.K_DOWN:
                                self.input_down = False
                    await self.send_input()
                    
                    self.draw()
                    self.clock.tick(FPS)
            except Exception as ex:
                print(ex)
            finally:
                recieve_task.cancel()
        pygame.quit()
    
    def draw(self):
        self.window.fill(BLACK)
        
        pygame.draw.rect(self.window, WHITE, 
                         (self.state["left_x"], self.state["left_y"], 
                          self.state["paddle_width"], self.state["paddle_height"]))
        pygame.draw.rect(self.window, WHITE, 
                         (self.state["right_x"], self.state["right_y"], 
                          self.state["paddle_width"], self.state["paddle_height"]))
        
        pygame.draw.circle(self.window, WHITE, 
                           (self.state["ball_x"], self.state["ball_y"]),
                           self.state["ball_radius"])
        
        role_text = self.normal_font.render(self.side, True, WHITE)
        self.window.blit(role_text, (10,10))
        
        if self.info_msg:
            info_text = self.font.render(self.info_msg, True, WHITE)
            self.window.blit(info_text, (10, HEIGHT - 30))
            
        pygame.display.update()
   
def parse_args():
    ap = argparse.ArgumentParser(description="Pong Websocket Client")
    ap.add_argument("--host", default="127.0.0.1", help="Szerver host (alap: localhost)")
    ap.add_argument("--port", type = int, default=8000, help="Szerver port (alap: 8000)")
    ap.add_argument("--room", default="default", help="Room azonosító (alap: default)")
    ap.add_argument("--name", default="Player", help="Játékosnév (alap: Player)")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    url = f"ws://{args.host}:{args.port}/ws?room_id={args.room}&name={args.name}"
    print(url)
    client = GameClient(url)
    try:
        asyncio.run(client.mainloop())
    except Exception as ex:
        print(ex)
        