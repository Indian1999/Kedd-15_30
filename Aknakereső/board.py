from cell import Cell
from random import sample
class Board:
    def __init__(self, rows, cols, mines_count):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines_count
        self.grid = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]
        
    def place_mines(self, safe_x, safe_y):
        positions = [(i, j) for j in range(self.cols) for i in range(self.rows)]
        positions.remove((safe_x, safe_y))
        mines = sample(positions, self.mines_count)
        for i, j in mines:
            self.grid[i][j].has_mine = True
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].adjacent_mines = self.count_adjacent_mines(i, j)
    
    def count_adjacent_mines(self, x, y):
        count = 0
        for i in range(-1, 2): # -1, 0, 1
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if x + i >= 0 and x + i < self.rows and y + j >= 0 and y+ j < self.cols:
                        if self.grid[x + i][y + j].has_mine:
                            count += 1
        return count
        