import pygame
import sys
import os
import math
pygame.font.init()

score_font = pygame.font.SysFont("Arial", 30)

# 0 - üres hely bogyóval
# 1 - fal
# 2 - packman kezdőhelye, ahol már járt korábban
# 3 - üres hely bogyó nélkül
# 4 - Szelem spawn hely ajtaja
# 5 - Power UP bogyó
level = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,5,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,2,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,4,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,3,3,3,1,0,0,0,5,1,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,1,5,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
TILE_SIZE = 32
WIDTH, HEIGHT = len(level[0]) * TILE_SIZE, len(level) * (TILE_SIZE + 4)

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WALL_COLOR = (0, 0, 255) # Kék
FOOD_COLOR = (255, 255, 255) # Fehér
PATH_COLOR = (0, 0, 0) # Fekete

img_folder = os.path.join(os.path.dirname(__file__), "images")
pacman_images = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(img_folder, "pacman1.png")),
        (TILE_SIZE, TILE_SIZE)
        ),
    pygame.transform.scale(
        pygame.image.load(os.path.join(img_folder, "pacman2.png")),
        (TILE_SIZE, TILE_SIZE)
        )
]

def find_start_position():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 2:
                return i, j
pacman_y, pacman_x = find_start_position()
score = 0

delta_x = 0
delta_y = 0

frame_counter = 0
current_pacman_image_index = 0

def draw_level():
    for i in range(len(level)):
        for j in range(len(level[i])):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if level[i][j] == 1:
                pygame.draw.rect(window, WALL_COLOR, rect)
            elif level[i][j] == 0:
                pygame.draw.circle(window, FOOD_COLOR, rect.center, TILE_SIZE / 8)

def can_move_to(x, y):
    return level[y][x] != 1

while True:
    window.fill(PATH_COLOR)
    draw_level()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and can_move_to(pacman_x - 1, pacman_y):
                delta_x, delta_y = -1, 0
            if event.key == pygame.K_RIGHT and can_move_to(pacman_x + 1, pacman_y):
                delta_x, delta_y = 1, 0
            if event.key == pygame.K_UP and can_move_to(pacman_x, pacman_y - 1):
                delta_x, delta_y = 0, -1
            if event.key == pygame.K_DOWN and can_move_to(pacman_x, pacman_y + 1):
                delta_x, delta_y = 0, 1
                
            
    new_x = pacman_x + delta_x
    new_y = pacman_y + delta_y
    if can_move_to(new_x, new_y):
        pacman_x = new_x
        pacman_y = new_y
        if level[pacman_y][pacman_x] == 0:
            level[pacman_y][pacman_x] = 2
            score += 10
    #else: Azért kommenteltük ki, hogy a pacman, irányban maradjon, ha falnak ütközik
    #    delta_x = 0
    #    delta_y = 0
    
    frame_counter += 1
    if frame_counter % 3 == 0:
        current_pacman_image_index += 1
        current_pacman_image_index %= len(pacman_images)
    
    pacman_img = pacman_images[current_pacman_image_index]
    angle_radian = math.atan2(delta_y, delta_x)
    angle_degree = math.degrees(angle_radian)
    pacman_img = pygame.transform.rotate(pacman_img, angle_degree)
    pacman_img = pygame.transform.flip(pacman_img, False, True)
    window.blit(pacman_img, (pacman_x * TILE_SIZE, pacman_y * TILE_SIZE))
    
    score_text = score_font.render(f"Score: {score}", True, FOOD_COLOR)
    window.blit(score_text, (TILE_SIZE // 2, HEIGHT - TILE_SIZE * 1.4))
    
            
    pygame.display.update()
    clock.tick(7)
