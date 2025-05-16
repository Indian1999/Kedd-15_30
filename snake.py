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

def gameloop():
    game_over = False
    application_close = False
    
    while not application_close:
        clock.tick(SPEED)
        while game_over:
            # Kiírjuk hogy új játék vagy bezárás
            pass
        
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    gameloop()
