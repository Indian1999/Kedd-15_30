import pygame
import os
import math
import random
pygame.font.init()
pygame.mixer.init()

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

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("arial", 40)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space fight")

ASSETS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(ASSETS_PATH, "assets")

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "laser.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "explosion.wav"))

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

METEOR_HEIGHT, METEOR_WIDTH = 50, 50
METEOR_VEL = 2
METEOR_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "meteor.png"))
METEOR_IMAGE = pygame.transform.scale(METEOR_IMAGE, (METEOR_WIDTH, METEOR_HEIGHT))
METEOR_IMAGE = pygame.transform.rotate(METEOR_IMAGE, 90)

METEOR_1_DIR = random.randint(0, 359)
METEOR_1_X_VEL = math.cos(METEOR_1_DIR) * METEOR_VEL
METEOR_1_Y_VEL = math.sin(METEOR_1_DIR) * METEOR_VEL
METEOR_2_DIR = random.randint(0, 359)
METEOR_2_X_VEL = math.cos(METEOR_2_DIR) * METEOR_VEL
METEOR_2_Y_VEL = math.sin(METEOR_2_DIR) * METEOR_VEL
METEOR_3_DIR = random.randint(0, 359)
METEOR_3_X_VEL = math.cos(METEOR_3_DIR) * METEOR_VEL
METEOR_3_Y_VEL = math.sin(METEOR_3_DIR) * METEOR_VEL

SHIELD_HEIGHT, SHIELD_WIDTH = 100, 120
SHIELD_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "shield.png"))
SHIELD_IMAGE = pygame.transform.scale(SHIELD_IMAGE, (SHIELD_WIDTH, SHIELD_HEIGHT))

red_shield_active = False
yellow_shield_active = False

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, meteor_1, meteor_2, meteor_3):
    WINDOW.blit(SPACE, (0,0))
    
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, WHITE)
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    
    WINDOW.blit(METEOR_IMAGE, (meteor_1.x, meteor_1.y))
    WINDOW.blit(METEOR_IMAGE, (meteor_2.x, meteor_2.y))
    WINDOW.blit(METEOR_IMAGE, (meteor_3.x, meteor_3.y))
    
    WINDOW.blit(RED_SPACEHIP, (red.x, red.y))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    
    if red_shield_active:
        WINDOW.blit(SHIELD_IMAGE, 
                    (red.x - (SHIELD_WIDTH - SPACESHIP_WIDTH) // 2 - 8,
                     red.y - (SHIELD_HEIGHT - SPACESHIP_HEIGHT) // 2 +8) )
    if yellow_shield_active:
        WINDOW.blit(SHIELD_IMAGE, 
                    (yellow.x - (SHIELD_WIDTH - SPACESHIP_WIDTH) // 2 - 8,
                     yellow.y - (SHIELD_HEIGHT - SPACESHIP_HEIGHT) // 2 +8) )
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
     
def handle_bullets(yellow_bullets, red_bullets, yellow, red, meteor_1, meteor_2, meteor_3):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if meteor_1.colliderect(bullet) or meteor_2.colliderect(bullet) or meteor_3.colliderect(bullet):
            yellow_bullets.remove(bullet)
          
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY  
        if bullet.x < 0:
            red_bullets.remove(bullet)
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if meteor_1.colliderect(bullet) or meteor_2.colliderect(bullet) or meteor_3.colliderect(bullet):
            red_bullets.remove(bullet)
            
    if yellow.colliderect(meteor_1):
        meteor_1.x = WIDTH + 40
        meteor_1.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(YELLOW_HIT))
    if yellow.colliderect(meteor_2):
        meteor_2.x = WIDTH + 40
        meteor_2.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(YELLOW_HIT))
    if yellow.colliderect(meteor_3):
        meteor_3.x = WIDTH + 40
        meteor_3.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(YELLOW_HIT))
            
    if red.colliderect(meteor_1):
        meteor_1.x = -40
        meteor_1.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(RED_HIT))
    if red.colliderect(meteor_2):
        meteor_2.x = -40
        meteor_2.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(RED_HIT))
    if red.colliderect(meteor_3):
        meteor_3.x = -40
        meteor_3.y = random.randint(0, HEIGHT)
        pygame.event.post(pygame.event.Event(RED_HIT))
        

def draw_winner(text):
    font = pygame.font.SysFont("arial", 100)
    rendered = font.render(text, True, WHITE)
    left = WIDTH // 2 - rendered.get_width() // 2
    top = HEIGHT // 2 - rendered.get_height() // 2
    WINDOW.blit(rendered, (left, top))
    pygame.display.update()
    pygame.time.delay(5000)
    
def meteor_controller(meteor_1, meteor_2, meteor_3):
    global METEOR_1_Y_VEL, METEOR_1_X_VEL, METEOR_2_Y_VEL, METEOR_2_X_VEL, METEOR_3_Y_VEL, METEOR_3_X_VEL
    meteor_1.x += METEOR_1_X_VEL
    meteor_1.y += METEOR_1_Y_VEL
    meteor_2.x += METEOR_2_X_VEL
    meteor_2.y += METEOR_2_Y_VEL
    meteor_3.x += METEOR_3_X_VEL
    meteor_3.y += METEOR_3_Y_VEL
    
    if meteor_1.x > WIDTH + 40:
        meteor_1.x = -40
        METEOR_1_DIR = random.randint(0, 359)
        METEOR_1_X_VEL = math.cos(METEOR_1_DIR) * METEOR_VEL
        METEOR_1_Y_VEL = math.sin(METEOR_1_DIR) * METEOR_VEL
    if meteor_1.x < -40:
        meteor_1.x = WIDTH + 40
        METEOR_1_DIR = random.randint(0, 359)
        METEOR_1_X_VEL = math.cos(METEOR_1_DIR) * METEOR_VEL
        METEOR_1_Y_VEL = math.sin(METEOR_1_DIR) * METEOR_VEL
    if meteor_1.y > HEIGHT + 40:
        meteor_1.y = -40
        METEOR_1_DIR = random.randint(0, 359)
        METEOR_1_X_VEL = math.cos(METEOR_1_DIR) * METEOR_VEL
        METEOR_1_Y_VEL = math.sin(METEOR_1_DIR) * METEOR_VEL
    if meteor_1.y < -40:
        meteor_1.y = HEIGHT + 40
        METEOR_1_DIR = random.randint(0, 359)
        METEOR_1_X_VEL = math.cos(METEOR_1_DIR) * METEOR_VEL
        METEOR_1_Y_VEL = math.sin(METEOR_1_DIR) * METEOR_VEL
        
    if meteor_2.x > WIDTH + 40:
        meteor_2.x = -40
        METEOR_2_DIR = random.randint(0, 359)
        METEOR_2_X_VEL = math.cos(METEOR_2_DIR) * METEOR_VEL
        METEOR_2_Y_VEL = math.sin(METEOR_2_DIR) * METEOR_VEL
    if meteor_2.x < -40:
        meteor_2.x = WIDTH + 40
        METEOR_2_DIR = random.randint(0, 359)
        METEOR_2_X_VEL = math.cos(METEOR_2_DIR) * METEOR_VEL
        METEOR_2_Y_VEL = math.sin(METEOR_2_DIR) * METEOR_VEL
    if meteor_2.y > HEIGHT + 40:
        meteor_2.y = -40
        METEOR_2_DIR = random.randint(0, 359)
        METEOR_2_X_VEL = math.cos(METEOR_2_DIR) * METEOR_VEL
        METEOR_2_Y_VEL = math.sin(METEOR_2_DIR) * METEOR_VEL
    if meteor_2.y < -40:
        meteor_2.y = HEIGHT + 40
        METEOR_2_DIR = random.randint(0, 359)
        METEOR_2_X_VEL = math.cos(METEOR_2_DIR) * METEOR_VEL
        METEOR_2_Y_VEL = math.sin(METEOR_2_DIR) * METEOR_VEL
        
    if meteor_3.x > WIDTH + 40:
        meteor_3.x = -40
        METEOR_3_DIR = random.randint(0, 359)
        METEOR_3_X_VEL = math.cos(METEOR_3_DIR) * METEOR_VEL
        METEOR_3_Y_VEL = math.sin(METEOR_3_DIR) * METEOR_VEL
    if meteor_3.x < -40:
        meteor_3.x = WIDTH + 40
        METEOR_3_DIR = random.randint(0, 359)
        METEOR_3_X_VEL = math.cos(METEOR_3_DIR) * METEOR_VEL
        METEOR_3_Y_VEL = math.sin(METEOR_3_DIR) * METEOR_VEL
    if meteor_3.y > HEIGHT + 40:
        meteor_3.y = -40
        METEOR_3_DIR = random.randint(0, 359)
        METEOR_3_X_VEL = math.cos(METEOR_3_DIR) * METEOR_VEL
        METEOR_3_Y_VEL = math.sin(METEOR_3_DIR) * METEOR_VEL
    if meteor_3.y < -40:
        meteor_3.y = HEIGHT + 40
        METEOR_3_DIR = random.randint(0, 359)
        METEOR_3_X_VEL = math.cos(METEOR_3_DIR) * METEOR_VEL
        METEOR_3_Y_VEL = math.sin(METEOR_3_DIR) * METEOR_VEL


def main():
    global yellow_shield_active
    red = pygame.Rect(WIDTH - 150, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(SPACESHIP_WIDTH + 20, HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    meteor_1 = pygame.Rect(WIDTH // 2, HEIGHT // 2, METEOR_WIDTH, METEOR_HEIGHT)
    meteor_2 = pygame.Rect(WIDTH // 2, HEIGHT // 2, METEOR_WIDTH, METEOR_HEIGHT)
    meteor_3 = pygame.Rect(WIDTH // 2, HEIGHT // 2, METEOR_WIDTH, METEOR_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    gameOn = True
    tick_counter = 0
    yellow_last_active = None
    red_last_active = None
    while gameOn:
        clock.tick(FPS)    
        tick_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_LSHIFT:
                    yellow_shield_active = True
                    yellow_last_active = tick_counter
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()
        
        if red_health <= 0:
            draw_winner("Yellow wins!")
            break
        if yellow_health <= 0:
            draw_winner("Red wins!")
            break
        
        if yellow_last_active and tick_counter > yellow_last_active + 300:
            yellow_shield_active = False
        
        keys_pressed = pygame.key.get_pressed()
        yellow_control(keys_pressed, yellow)
        red_control(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, meteor_1, meteor_2, meteor_3)
        meteor_controller(meteor_1, meteor_2, meteor_3)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, meteor_1, meteor_2, meteor_3)

if __name__ == "__main__":
    main()