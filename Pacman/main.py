import pygame
import sys
import os
import getpass
import time
import math
import requests
import random
import hashlib

pygame.font.init()

score_font = pygame.font.SysFont("Arial", 30)

TILE_SIZE = 32
LEVEL_ROWS, LEVEL_COLS = 15, 20
WIDTH, HEIGHT = LEVEL_COLS * TILE_SIZE, LEVEL_ROWS * (TILE_SIZE + 4)
FPS = 7

URL = "https://pacman-a10cd-default-rtdb.europe-west1.firebasedatabase.app/highscores.json"

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

def code_timestamp(timestamp):
    hash_object = hashlib.sha256(str(timestamp).encode())
    return hash_object.hexdigest()

def spawn_initial_ghosts(level, ghosts):
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 3 or level[i][j] == 6:
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                ghosts.append(rect)
           
def find_start_position(level):
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 2:
                return i, j

def find_enemy_spawn_position(level):
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 6:
                return i, j

def matrix_pos_from_window_pos(x, y):
    matrix_row = y // TILE_SIZE
    matrix_col = x // TILE_SIZE
    return (matrix_row, matrix_col)

def can_ghost_move_to(x, y, level):
    return level[x][y] != 1

def fastest_neighbour(distances, x, y):
    values = []
    if distances[y+1][x] != -1:
        values.append(distances[y+1][x])
    if distances[y-1][x] != -1:
        values.append(distances[y-1][x])
    if distances[y][x+1] != -1:
        values.append(distances[y][x+1])
    if distances[y][x-1] != -1:
        values.append(distances[y][x-1])
    return min(values)
    
def possible_moves(distances, x, y):
    moves = []
    if distances[y+1][x] != -1 and distances[y + 1][x] > distances[y][x] + 1:
        moves.append((y+1, x))
    if distances[y-1][x] != -1 and distances[y - 1][x] > distances[y][x] + 1:
        moves.append((y-1, x))
    if distances[y][x+1] != -1 and distances[y][x+1] > distances[y][x] + 1:
        moves.append((y, x+1))
    if distances[y][x-1] != -1 and distances[y][x-1] > distances[y][x] + 1:
        moves.append((y, x-1))
    return moves
        
def find_distances(distances, x, y):
    possible_new_value = fastest_neighbour(distances, x, y) + 1
    if distances[y][x] > possible_new_value:
        distances[y][x] = possible_new_value
    moves = possible_moves(distances, x, y)
    for move in moves:
        find_distances(distances, move[1], move[0])
    
def choose_random_value(values):
    if random.random() < 0.8:
        return min(values)
    else:
        return random.choice(values)
    
def find_direction(ghost_x, ghost_y, pacman_x, pacman_y, level, power_up_active):
    distances = [[math.inf for j in range(len(level[0]))] for i in range(len(level))]
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                distances[i][j] = -1 # -1-el jelöljük a falat
    distances[pacman_y][pacman_x] = 0
    find_distances(distances, pacman_x, pacman_y)
    
    values = [distances[ghost_y+1][ghost_x], 
              distances[ghost_y-1][ghost_x],
              distances[ghost_y][ghost_x+1],
              distances[ghost_y][ghost_x-1]
              ]
    while -1 in values:
        values.remove(-1)
    best_value = choose_random_value(values)
    if power_up_active:
        best_value = random.choice(values)
    if distances[ghost_y+1][ghost_x] == best_value:
        return (1, 0)
    if distances[ghost_y-1][ghost_x] == best_value:
        return (-1, 0)
    if distances[ghost_y][ghost_x+1] == best_value:
        return (0, 1)
    if distances[ghost_y][ghost_x-1] == best_value:
        return (0, -1)
    
def move_ghosts(ghosts, score, ghost_worth, level, pacman_y, pacman_x, enemy_spawn_y, enemy_spawn_x, power_up_active):
    for ghost in ghosts:
        #directions = [(0, 1), (1, 0), (0,-1), (-1, 0)]
        #dy, dx = random.choice(directions)
        ghost_row, ghost_col = matrix_pos_from_window_pos(ghost.x, ghost.y)
        dy, dx = find_direction(ghost_col, ghost_row, pacman_x, pacman_y, level, power_up_active)
        if can_ghost_move_to(ghost_row + dy, ghost_col + dx, level):
            ghost.x += dx * TILE_SIZE
            ghost.y += dy * TILE_SIZE
        if pacman_y == ghost_row and pacman_x ==  ghost_col:
            if power_up_active:
                ghost.y = enemy_spawn_y * TILE_SIZE
                ghost.x = enemy_spawn_x * TILE_SIZE
                score += ghost_worth
                ghost_worth *= 2
            else:
                return False, score
    return True, score
          
def has_food_left(level):
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 0 or level[i][j] == 5:
                return True
    return False

def activate_power_up(activation_timestamp):
    global power_up_active, frame_counter
    power_up_active = True
    while activation_timestamp + POWER_UP_UPTIME > frame_counter:
        pass
    power_up_active = False

def draw_level(level, ghosts, power_up_active):
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
                     
def draw_game_over(score, win):
    def post_action():
        data = {
            "username": getpass.getuser(),
            "score": score,
            "timestamp": time.time()
        }
        try:
            response = requests.post(URL, json=data)
            if response.status_code == 200:
                print("Highscore submitted successfully!")
            else:
                print("Error:", response.status_code)
        except Exception as ex:
            print("Error:", ex)
            
    post_action()
    window.fill(PATH_COLOR)
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, FOOD_COLOR)
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2,
                             score_text.get_height() // 2 + 40
                             ))
    if win:
        win_text = font.render("You Win!", True, FOOD_COLOR)
        window.blit(win_text, (WIDTH // 2 - score_text.get_width() // 2,
                               score_text.get_height() // 2
                             ))
    else:
        win_text = font.render("You Lose!", True, FOOD_COLOR)
        window.blit(win_text, (WIDTH // 2 - score_text.get_width() // 2,
                               score_text.get_height() // 2
                             ))
    highscore_text = font.render("Highscores:", True, FOOD_COLOR)
    window.blit(highscore_text, (WIDTH // 2 - score_text.get_width() // 2,
                                 score_text.get_height() // 2 + 80
                                 ))
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
        else:
            print("Error:", response.status_code)
    except Exception as ex:
        print("Error:", ex)
    sorted_scores = sorted(data.items(), key = lambda x: x[1]["score"], reverse = True)
    i = 0
    while i < 10 and i < len(sorted_scores):
        key, entry = sorted_scores[i]
        name, score = entry["username"], entry["score"]
        entry_text = font.render(f"{i+1}. {name}: {score}", True, (50, 250 - i * 15, 50))
        window.blit(entry_text, (WIDTH // 2 - score_text.get_width() // 2,
                                 score_text.get_height() // 2 + 120 + i * 40
                                 ))
        i += 1
        
    pygame.display.update()

def can_move_to(x, y, level):
    return level[y][x] != 1 and level[y][x] != 4

def main():
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
    score = 0
    ghost_worth = 200
    gameOn = True

    delta_x = 0
    delta_y = 0 
        
    ghosts = []
    spawn_initial_ghosts(level, ghosts)
    pacman_y, pacman_x = find_start_position(level)
    enemy_spawn_y, enemy_spawn_x = find_enemy_spawn_position(level)

    power_up_active = False
    last_power_up = 0
    POWER_UP_UPTIME = FPS * 10
    frame_counter = 0
    current_pacman_image_index = 0
    while True:
        while not gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()

        window.fill(PATH_COLOR)
        draw_level(level, ghosts, power_up_active)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_move_to(pacman_x - 1, pacman_y, level):
                    delta_x, delta_y = -1, 0
                if event.key == pygame.K_RIGHT and can_move_to(pacman_x + 1, pacman_y, level):
                    delta_x, delta_y = 1, 0
                if event.key == pygame.K_UP and can_move_to(pacman_x, pacman_y - 1, level):
                    delta_x, delta_y = 0, -1
                if event.key == pygame.K_DOWN and can_move_to(pacman_x, pacman_y + 1, level):
                    delta_x, delta_y = 0, 1

        new_x = pacman_x + delta_x
        new_y = pacman_y + delta_y
        if can_move_to(new_x, new_y, level):
            pacman_x = new_x
            pacman_y = new_y
            if level[pacman_y][pacman_x] == 0:
                level[pacman_y][pacman_x] = 3
                score += 10
            elif level[pacman_y][pacman_x] == 5:
                level[pacman_y][pacman_x] = 3
                power_up_active = True
                last_power_up = frame_counter
        gameOn, score = move_ghosts(ghosts, score, ghost_worth, level, 
                    pacman_y, pacman_x, enemy_spawn_y, enemy_spawn_x, power_up_active)


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

        if not has_food_left(level) and not power_up_active:
            gameOn = False
            draw_game_over(score, True)
        if has_food_left(level) and not gameOn:
            draw_game_over(score, False)

        pygame.display.update()
        clock.tick(FPS)
main()