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
            
    async def mainloop(self):
        async with websockets.connect(self.url) as ws:
            self.ws = ws
            