import pygame
import sys
import os
import math
import random
pygame.font.init()

score_font = pygame.font.SysFont("Arial", 30)

# 0 - üres hely bogyóval
# 1 - fal
# 2 - packman kezdőhelye, (ahol már járt korábban)
# 3 - üres hely bogyó nélkül
# 4 - Szelem spawn hely ajtaja
# 5 - Power UP bogyó
# 6 - Szellem spawn location
level = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,5,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,2,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,4,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,3,6,3,1,0,0,0,5,1,0,1],
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
FPS = 7


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
ghost_image = pygame.transform.scale(
    pygame.image.load(os.path.join(img_folder, "ghost.png")),
    (TILE_SIZE, TILE_SIZE)
)
scared_ghost_image = pygame.transform.scale(
    pygame.image.load(os.path.join(img_folder, "ghost_scared.png")),
    (TILE_SIZE, TILE_SIZE)
)
def lose():
    pygame.quit()
    exit()

def spawn_initial_ghosts():
    global ghosts
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 3 or level[i][j] == 6:
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                ghosts.append(rect)
                
ghosts = []
spawn_initial_ghosts()
def find_start_position():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 2:
                return i, j
pacman_y, pacman_x = find_start_position()

def find_enemy_spawn_position():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 6:
                return i, j
enemy_spawn_y, enemy_spawn_x = find_enemy_spawn_position()

def matrix_pos_from_window_pos(x, y):
    matrix_row = y // TILE_SIZE
    matrix_col = x // TILE_SIZE
    return (matrix_row, matrix_col)

def can_ghost_move_to(x, y):
    return level[x][y] != 1

def move_ghosts():
    global ghosts, score, ghost_worth
    for ghost in ghosts:
        directions = [(0, 1), (1, 0), (0,-1), (-1, 0)]
        dy, dx = random.choice(directions)
        ghost_row, ghost_col = matrix_pos_from_window_pos(ghost.x, ghost.y)
        if can_ghost_move_to(ghost_row + dy, ghost_col + dx):
            ghost.x += dx * TILE_SIZE
            ghost.y += dy * TILE_SIZE
        if pacman_y == ghost_row and pacman_x ==  ghost_col:
            if power_up_active:
                ghost.y = enemy_spawn_y * TILE_SIZE
                ghost.x = enemy_spawn_x * TILE_SIZE
                score += ghost_worth
                ghost_worth *= 2
            else:
                lose()
                
score = 0
ghost_worth = 200

delta_x = 0
delta_y = 0

power_up_active = False
last_power_up = 0
POWER_UP_UPTIME = FPS * 10
frame_counter = 0
current_pacman_image_index = 0

def activate_power_up(activation_timestamp):
    global power_up_active, frame_counter
    power_up_active = True
    while activation_timestamp + POWER_UP_UPTIME > frame_counter:
        pass
    power_up_active = False

def draw_level():
    for i in range(len(level)):
        for j in range(len(level[i])):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if level[i][j] == 1: # fal
                pygame.draw.rect(window, WALL_COLOR, rect)
            elif level[i][j] == 0: # kaja
                pygame.draw.circle(window, FOOD_COLOR, rect.center, TILE_SIZE / 8)
            elif level[i][j] == 5: # power up
                pygame.draw.circle(window, FOOD_COLOR, rect.center, TILE_SIZE / 4)
            elif level[i][j] == 4:
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE // 8)
                pygame.draw.rect(window, (180, 180, 180), rect)
    for ghost in ghosts:
        if not power_up_active:
            window.blit(ghost_image, ghost)
        else:
            window.blit(scared_ghost_image, ghost)
                
            

def can_move_to(x, y):
    return level[y][x] != 1 and level[y][x] != 4

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
            level[pacman_y][pacman_x] = 3
            score += 10
        elif level[pacman_y][pacman_x] == 5:
            level[pacman_y][pacman_x] = 3
            power_up_active = True
            last_power_up = frame_counter
    move_ghosts()
    
            
    #else: Azért kommenteltük ki, hogy a pacman, irányban maradjon, ha falnak ütközik
    #    delta_x = 0
    #    delta_y = 0
    
    frame_counter += 1
    if frame_counter % 3 == 0:
        current_pacman_image_index += 1
        current_pacman_image_index %= len(pacman_images)
    if frame_counter > last_power_up + POWER_UP_UPTIME:
        power_up_active = False
    
    pacman_img = pacman_images[current_pacman_image_index]
    angle_radian = math.atan2(delta_y, delta_x)
    angle_degree = math.degrees(angle_radian)
    pacman_img = pygame.transform.rotate(pacman_img, angle_degree)
    pacman_img = pygame.transform.flip(pacman_img, False, True)
    window.blit(pacman_img, (pacman_x * TILE_SIZE, pacman_y * TILE_SIZE))
    
    score_text = score_font.render(f"Score: {score}", True, FOOD_COLOR)
    window.blit(score_text, (TILE_SIZE // 2, HEIGHT - TILE_SIZE * 1.4))
    
            
    pygame.display.update()
    clock.tick(FPS)
