import pygame
from board import Board
pygame.font.init()

WIDTH, HEIGHT  = 400, 400
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
NUM_MINES = 40

REVEALED_COLOR = (200, 200, 200)
UNREVEALED_COLOR = (100, 100, 100)
FLAG_COLOR = (255, 0, 0)
MINE_COLOR = (0, 0, 0)
BASE_COLOR = (0, 0, 0)
BORDER_COLOR = (50, 50, 50)

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
                
            pygame.draw.rect(window, BORDER_COLOR, rect, 1)
                
            if cell.flagged and not cell.revealed:
                pygame.draw.circle(window, FLAG_COLOR, rect.center, CELL_SIZE // 3)
                
            if cell.has_mine and cell.revealed:
                pygame.draw.circle(window, MINE_COLOR, rect.center, CELL_SIZE // 3)
                
            if cell.revealed and cell.adjacent_mines > 0 and not cell.has_mine:
                text = number_font.render(str(cell.adjacent_mines), True, get_num_color(cell.adjacent_mines))
                text_rect = text.get_rect(center=rect.center)
                window.blit(text, text_rect)
            
def cell_clicked(mouse_pos, button):
    global gameOn
    x = mouse_pos[0] // CELL_SIZE
    y = mouse_pos[1] // CELL_SIZE
    
    if x >= 0 and x < ROWS and y >= 0 and y < COLS:
        if not board.mines_placed:
            board.place_mines(x, y)
            
        if button == 1 and not board.grid[x][y].revealed: # bal klick
            if board.grid[x][y].has_mine:
                board.grid[x][y].revealed = True
                gameOn = False
            else:
                board.grid[x][y].revealed = True
        elif button == 3: # jobb klick
            board.grid[x][y].flagged = not board.grid[x][y].flagged
            
gameOn = True         
while True:   
    window.fill((BASE_COLOR))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if gameOn and event.type == pygame.MOUSEBUTTONDOWN:
            cell_clicked(pygame.mouse.get_pos(), event.button)
        
    draw_board()
    pygame.display.update()
    clock.tick(60)
            
            

