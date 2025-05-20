import pygame
from board import Board
pygame.font.init()

WIDTH, HEIGHT  = 400, 400
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
NUM_MINES = 10

REVEALED_COLOR = (200, 200, 200)
UNREVEALED_COLOR = (100, 100, 100)
FLAG_COLOR = (255, 0, 0)
MINE_COLOR = (0, 0, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aknakereső")
clock = pygame.time.Clock()

number_font = pygame.font.SysFont("Arial", CELL_SIZE // 2)

board = Board(ROWS, COLS, NUM_MINES)

def get_num_color(num):
    if num == 1:
        return (0,0,255)
    if num == 2:
        return (0,128,0)
    if num == 3:
        return (255,0,0)
    if num == 4:
        return (0,0,128)
    if num == 5:
        return (128,0,0)
    if num == 6:
        return (0,128,128)
    if num == 7:
        return (0,0,0)
    if num == 8:
        return (128,128,128)
    

def draw_board():
    for i in range(ROWS):
        for j in range(COLS):
            cell = board.grid[i][j]
            rect = pygame.Rect(i * CELL_SIZE, j *CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if cell.revealed:
                pygame.draw.rect(window, REVEALED_COLOR, rect)
            else:
                pygame.draw.rect(window, UNREVEALED_COLOR, rect)
                
            if cell.flagged and not cell.revealed:
                pygame.draw.circle(window, FLAG_COLOR, rect.center, CELL_SIZE // 3)
                
            if cell.has_mine and cell.revealed:
                pygame.draw.circle(window, MINE_COLOR, rect.center, CELL_SIZE // 3)
                
            if cell.revealed and cell.adjacent_mines > 0:
                text = number_font.render(str(cell.adjacent_mines), True, get_num_color(cell.adjacent_mines))
            
                
             
while True:   
    draw_board()


