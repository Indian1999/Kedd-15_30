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

PIXEL_SIZE = 10
SPEED = 15

game_over_font = pygame.font.SysFont("Arial", 25)
score_font = pygame.font.SysFont("Arial", 35)

def random_pos():
    x = random.randrange(0, WINDOW_WIDTH, PIXEL_SIZE)
    y = random.randrange(0, WINDOW_HEIGHT, PIXEL_SIZE)
    return x, y

def gameloop():
    game_over = False
    application_close = False
    
    x_snake = WINDOW_WIDTH // 2
    y_snake = WINDOW_HEIGHT // 2
    
    x_change = 0
    y_change = 0
    
    snake = []
    length_of_snake = 1
    
    x_food, y_food = random_pos()
    
    while not application_close:
        clock.tick(SPEED)
        while game_over:
            # Kiírjuk hogy új játék vagy bezárás
            pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -PIXEL_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = PIXEL_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -PIXEL_SIZE
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = PIXEL_SIZE
        
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    gameloop()
