import pygame
import os
import math
import random

WIDTH = 900
HEIGHT = 500

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH = 80
SPACESHIP_HEIGHT = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space fight")

ASSETS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(ASSETS_PATH, "assets")

SPACE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "space.png")), (WIDTH, HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_red.png"))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_yellow.png"))
RED_SPACEHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90
)

def draw_window(red, yellow):
    WINDOW.blit(SPACE, (0,0))
    WINDOW.blit(RED_SPACEHIP, (red.x, red.y))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    pygame.display.update()

def main():
    red = pygame.Rect(WIDTH - 150, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(SPACESHIP_WIDTH + 20, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    clock = pygame.time.Clock()
    gameOn = True
    while gameOn:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
                pygame.quit()
                exit()
        
        keys_pressed = pygame.key.get_pressed()
        yellow_control(keys_pressed, yellow)
        red_control(keys_pressed, red)
        draw_window(red, yellow)

if __name__ == "__main__":
    main()