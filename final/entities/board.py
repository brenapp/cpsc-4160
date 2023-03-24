# board.py
#
# Author: Brendan McGuire
# Created 11 March 2023
#
# This entity represents the Tetris board in the game. Our implementation does not directly
# follow the Tetris Specification, but we take a lot of inspiration form it. The board is a 10x40
# grid of cells, but all cells above 20 are invisible.
#
#

from . import entity
import pygame

# Each tetromino is represented by a base tile, and a list of tiles relative to the base tile. This
# allows us to quickly move the tetromino around the board. Importantly, the base tile is the center
# of rotation for the tetromino, so be sure to select it appropriately.


class Tetromino:

    def __init__(self, id, base_tile, tiles, image):
        self.id = id
        self.base_tile = base_tile
        self.tiles = tiles
        self.image = image

    def get_absolute_tiles(self):
        return [(self.base_tile[0] + tile[0], self.base_tile[1] + tile[1]) for tile in self.tiles]

    def can_move(self, x, y):
        for tile in self.get_absolute_tiles():
            if tile[0] + x < 0 or tile[0] + x >= BOARD_WIDTH:
                return False
            if tile[1] + y < 0 or tile[1] + y >= BOARD_HEIGHT:
                return False

            if BOARD[tile[1] + y][tile[0] + x] is not None and BOARD[tile[1] + y][tile[0] + x] != self.id:
                return False

        return True

    def can_rotate(self, direction):
        if direction == "cw":
            tiles = [(tile[1], -tile[0]) for tile in self.tiles]
        elif direction == "ccw":
            tiles = [(-tile[1], tile[0]) for tile in self.tiles]

        for tile in tiles:
            (x, y) = (tile[0] + self.base_tile[0], tile[1] + self.base_tile[1])

            if x < 0 or x >= BOARD_WIDTH:
                return False
            if y < 0 or y >= BOARD_HEIGHT:
                return False

            if BOARD[y][x] is not None and BOARD[y][x] != self.id:
                return False

        return True

    def move(self, x, y):
        self.base_tile = (self.base_tile[0] + x, self.base_tile[1] + y)

    def rotate(self, direction):
        if direction == "cw":
            self.tiles = [(tile[1], -tile[0]) for tile in self.tiles]
        elif direction == "ccw":
            self.tiles = [(-tile[1], tile[0]) for tile in self.tiles]


# Represents the current state of the board. Each cell is either None (empty) or the index of
# the tetromino in the TETROMINOS array.
BOARD_WIDTH = 15
BOARD_HEIGHT = 25

BOARD = [[None for x in range(BOARD_WIDTH)]
         for y in range(BOARD_HEIGHT)]


# The width and height of each cell in the board
CELL_WIDTH = 30
CELL_HEIGHT = 30

BOARD_WIDTH_PX = CELL_WIDTH * BOARD_WIDTH
BOARD_HEIGHT_PX = CELL_HEIGHT * BOARD_HEIGHT
BOARD_X = CELL_WIDTH
BOARD_Y = CELL_HEIGHT
BOARD_COLOR = (255, 255, 255)
GRID_LINE_COLOR = (200, 200, 200)


class Board(entity.Entity):

    # Represents the currently in play tetrominos. Note that this array is sparse, and upon a
    # tetrominos being placed, the corresponding index will be set to None.
    TETROMINOS = []
    tetromino_count = 0

    rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH_PX, BOARD_HEIGHT_PX)

    RECTS = [[pygame.Rect(BOARD_X + x * CELL_WIDTH, BOARD_Y + y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
              for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

    def __init__(self, id, init_state):
        super().__init__(id, init_state)

    def add_tetromino(self, base_tile, tiles, image):
        tetromino = Tetromino(self.tetromino_count, base_tile, tiles, image)
        self.TETROMINOS.append(tetromino)

        base = tetromino.base_tile
        for tile in tetromino.tiles:
            BOARD[base[1] + tile[1]][base[0] +
                                     tile[0]] = self.tetromino_count
        self.tetromino_count += 1

    def move_tetromino(self, index, x, y):
        tetromino = self.TETROMINOS[index]

        if not tetromino.can_move(x, y):
            return

        for tile in tetromino.get_absolute_tiles():
            BOARD[tile[1]][tile[0]] = None
        tetromino.move(x, y)
        for tile in tetromino.get_absolute_tiles():
            BOARD[tile[1]][tile[0]] = index

    def rotate_tetromino(self, index, direction):
        tetromino = self.TETROMINOS[index]

        if not tetromino.can_rotate(direction):
            return

        for tile in tetromino.get_absolute_tiles():
            BOARD[tile[1]][tile[0]] = None
        tetromino.rotate(direction)
        for tile in tetromino.get_absolute_tiles():
            BOARD[tile[1]][tile[0]] = index

    def tetromino_is_active(self, index):
        return self.TETROMINOS[index] is not None and self.TETROMINOS[index].can_move(0, 1)

    def remove_tetromino(self, index):
        tiles = self.TETROMINOS[index].get_absolute_tiles()
        for tile in tiles:
            BOARD[tile[1]][tile[0]] = None
        self.TETROMINOS[index] = None

    def clear_lines(self):
        for y in range(BOARD_HEIGHT):
            if all([BOARD[y][x] is not None for x in range(BOARD_WIDTH)]):
                for x in range(BOARD_WIDTH):
                    BOARD[y][x] = None

                for y2 in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        BOARD[y2][x] = BOARD[y2 - 1][x]

    def update_state(self):
        pass

    def handle_event(self, event):
        pass

    def render(self, surface):

        # Draw the board
        pygame.draw.rect(surface, BOARD_COLOR, self.rect)

        # Draw grid lines
        for x in range(BOARD_WIDTH):
            pygame.draw.line(surface, GRID_LINE_COLOR, (BOARD_X + x *
                             CELL_WIDTH, BOARD_Y), (BOARD_X + x * CELL_WIDTH, BOARD_Y + BOARD_HEIGHT_PX))

        for y in range(BOARD_HEIGHT):
            pygame.draw.line(surface, GRID_LINE_COLOR, (BOARD_X,
                             BOARD_Y + y * CELL_HEIGHT), (BOARD_X + BOARD_WIDTH_PX, BOARD_Y + y * CELL_HEIGHT))

        # Draw the tetrominos
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if BOARD[y][x] is not None:
                    tetromino = self.TETROMINOS[BOARD[y][x]]
                    pygame.Surface.blit(
                        surface, tetromino.image, self.RECTS[y][x])
