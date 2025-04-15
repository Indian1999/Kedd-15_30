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

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space fight")

ASSETS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(ASSETS_PATH, "assets")

SPACE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "space.png")), (WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_red.png"))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship_yellow.png"))
RED_SPACEHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)

def draw_window(red, yellow, red_bullets, yellow_bullets):
    WINDOW.blit(SPACE, (0,0))
    
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    
    WINDOW.blit(RED_SPACEHIP, (red.x, red.y))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    pygame.display.update()

def yellow_control(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY >= 0:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + SPACESHIP_WIDTH + VELOCITY <= WIDTH / 2 + 20:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY >= 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + SPACESHIP_HEIGHT + VELOCITY <= HEIGHT - 15:
        yellow.y += VELOCITY
        
def red_control(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY >= WIDTH / 2:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + SPACESHIP_WIDTH + VELOCITY <= WIDTH + 20:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY >= 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + SPACESHIP_HEIGHT + VELOCITY <= HEIGHT - 15:
        red.y += VELOCITY
     
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
          
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY  
        if bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(WIDTH - 150, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(SPACESHIP_WIDTH + 20, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    gameOn = True
    while gameOn:
        clock.tick(FPS)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2, 10, 5)
                    red_bullets.append(bullet)
        
        keys_pressed = pygame.key.get_pressed()
        yellow_control(keys_pressed, yellow)
        red_control(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets)

if __name__ == "__main__":
    main()