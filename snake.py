import pygame
import random
pygame.font.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_WIDTH = 600
WINDOW_HEIGHT  = 400

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

PIXEL_SIZE = 40
SPEED = 10

game_over_font = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("Arial", 35)

def random_pos():
    x = random.randrange(0, WINDOW_WIDTH, PIXEL_SIZE)
    y = random.randrange(0, WINDOW_HEIGHT, PIXEL_SIZE)
    return x, y

def draw_snake(snake):
    for pixel in snake:
        pygame.draw.rect(WINDOW, BLACK, [pixel[0], pixel[1], PIXEL_SIZE, PIXEL_SIZE])
        
def draw_points(points):
    text = score_font.render("Score: " + str(points), True, YELLOW)
    WINDOW.blit(text, [0,0]) 

def gameloop():
    game_over = False
    application_close = False
    
    x_snake = round(WINDOW_WIDTH // 2 / PIXEL_SIZE) * PIXEL_SIZE
    y_snake = round(WINDOW_HEIGHT // 2 / PIXEL_SIZE) * PIXEL_SIZE
    
    x_change = 0
    y_change = 0
    
    snake = []
    length_of_snake = 1
    
    x_food, y_food = random_pos()
    
    while not application_close:
        clock.tick(SPEED)
        while game_over:
            WINDOW.fill(BLUE)
            text = game_over_font.render("R: újraindítás | Q: Kilépés", True, RED)
            WINDOW.blit(text, [WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2])
            draw_points(length_of_snake - 1)
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        application_close = True
                    if event.key == pygame.K_r:
                        gameloop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != PIXEL_SIZE:
                    x_change = -PIXEL_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -PIXEL_SIZE:
                    x_change = PIXEL_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != PIXEL_SIZE:
                    x_change = 0
                    y_change = -PIXEL_SIZE
                elif event.key == pygame.K_DOWN and y_change != -PIXEL_SIZE:
                    x_change = 0
                    y_change = PIXEL_SIZE
        
        # Leellenőrizzük, hogy kimentük-e a játéktérről
        if x_snake >= WINDOW_WIDTH or x_snake < 0 or y_snake >= WINDOW_HEIGHT or y_snake < 0:
            game_over = True
            
        # A sebességel módosítjuk a snake pozícióját
        x_snake += x_change
        y_snake += y_change
        
        WINDOW.fill(BLUE) # Legyen kék a háttér
        pygame.draw.rect(WINDOW, GREEN, [x_food, y_food, PIXEL_SIZE, PIXEL_SIZE]) # Kaja kirajzolása
        
        snake.append([x_snake, y_snake])
        if len(snake) > length_of_snake:
            del snake[0]
            
        # Saját farkába harapott-e a kígyó?
        for pixel in snake[:-1]:
            if pixel == snake[-1]:
                game_over = True
                
        draw_snake(snake)
        draw_points(length_of_snake - 1)
        
        # Ha a kígyó feje a kajánál van, egye meg
        if x_snake == x_food and y_snake == y_food:
            x_food, y_food = random_pos()
            length_of_snake += 1
        
        pygame.display.update()
        
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    gameloop()
