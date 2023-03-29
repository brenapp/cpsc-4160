from . import entity

# 

class Frog(entity.Entity):

    def __init__(self, board, frogX=0, frogY=0):
        self.position = [frogX, frogY]
        self.board = board

    def can_move(self, x, y, board):
        if self.position[0] + x < 0 or self.position[0] + x >= len(board[0]):
            return False
        if self.position[1] + y < 0 or self.position[1] + y >= len(board):
            return False
        new_pos = (self.position[0] + x, self.position[1] + y)
        if board[new_pos[1]][new_pos[0]] is not None and board[new_pos[1]][new_pos[0]] != self.index:
            return False

        return True

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)
