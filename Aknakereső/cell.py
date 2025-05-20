class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent_mines = 0