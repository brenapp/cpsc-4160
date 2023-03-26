
from . import entity

# Each tetromino is represented by a base tile, and a list of tiles relative to the base tile. This
# allows us to quickly move the tetromino around the board. Importantly, the base tile is the center
# of rotation for the tetromino, so be sure to select it appropriately.

I_PIECE = [(-1, 0), (0, 0), (1, 0), (2, 0)]
J_PIECE = [(-1, -1), (-1, 0), (0, 0), (1, 0)]
L_PIECE = [(-1, 0), (0, 0), (1, 0), (1, -1)]
O_PIECE = [(0, 0), (1, 0), (0, 1), (1, 1)]
S_PIECE = [(-1, 0), (0, 0), (0, 1), (1, 1)]
Z_PIECE = [(-1, 1), (-1, 0), (0, 0), (1, 0)]
T_PIECE = [(-1, 0), (0, 0), (1, 0), (0, 1)]
PIECES = [I_PIECE, J_PIECE, L_PIECE,  O_PIECE, S_PIECE, Z_PIECE, T_PIECE]


class Tetromino(entity.Entity):

    def __init__(self, index, base_tile, tiles, color):
        self.index = index
        self.base_tile = base_tile
        self.tiles = tiles
        self.color = color

    def get_absolute_tiles(self):
        return [(self.base_tile[0] + tile[0], self.base_tile[1] + tile[1]) for tile in self.tiles]

    def can_move(self, x, y, board):
        for tile in self.get_absolute_tiles():
            if tile[0] + x < 0 or tile[0] + x >= len(board[0]):
                return False
            if tile[1] + y < 0 or tile[1] + y >= len(board):
                return False
            new_pos = (tile[0] + x, tile[1] + y)
            if board[new_pos[1]][new_pos[0]] is not None and board[new_pos[1]][new_pos[0]] != self.index:
                return False

        return True

    def can_rotate(self, direction, board):
        if direction == "cw":
            tiles = [(tile[1], -tile[0]) for tile in self.tiles]
        elif direction == "ccw":
            tiles = [(-tile[1], tile[0]) for tile in self.tiles]

        for tile in tiles:
            (x, y) = (tile[0] + self.base_tile[0], tile[1] + self.base_tile[1])

            if x < 0 or x >= len(board[0]):
                return False
            if y < 0 or y >= len(board):
                return False

            if board[y][x] is not None and board[y][x] != self.index:
                return False

        return True

    def move(self, x, y):
        self.base_tile = (self.base_tile[0] + x, self.base_tile[1] + y)

    def rotate(self, direction):
        if direction == "cw":
            self.tiles = [(tile[1], -tile[0]) for tile in self.tiles]
        elif direction == "ccw":
            self.tiles = [(-tile[1], tile[0]) for tile in self.tiles]
