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

    def __init__(self, base_tile, tiles, color):
        self.base_tile = base_tile
        self.tiles = tiles
        self.color = color

    def get_absolute_tiles(self):
        return [(self.base_tile[0] + tile[0], self.base_tile[1] + tile[1]) for tile in self.tiles]

    def move(self, x, y):
        self.base_tile = (self.base_tile[0] + x, self.base_tile[1] + y)

    def rotate(self, direction):
        if direction == "cw":
            self.tiles = [(tile[1], -tile[0]) for tile in self.tiles]
        elif direction == "ccw":
            self.tiles = [(-tile[1], tile[0]) for tile in self.tiles]


BOARD_WIDTH = 20
BOARD_HEIGHT = 40
BOARD_HEIGHT_VISIBLE = 20

# The width and height of each cell in the board
CELL_WIDTH = 30
CELL_HEIGHT = 30

BOARD_WIDTH_PX = CELL_WIDTH * BOARD_WIDTH
BOARD_HEIGHT_PX = CELL_HEIGHT * BOARD_HEIGHT
BOARD_X = 0
BOARD_Y = 0
BOARD_COLOR = (255, 255, 255)


class Board(entity.Entity):

    # Represents the currently in play tetrominos. Note that this array is sparse, and upon a
    # tetrominos being placed, the corresponding index will be set to None.
    TETROMINOS = []
    tetromino_count = 0

    rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH_PX, BOARD_HEIGHT_PX)

    # Represents the current state of the board. Each cell is either None (empty) or the index of
    # the tetromino in the TETROMINOS array.
    BOARD = [[None for x in range(BOARD_WIDTH)]
             for y in range(BOARD_HEIGHT)]

    RECTS = [[pygame.Rect(BOARD_X + x * CELL_WIDTH, BOARD_Y + y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
              for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

    def __init__(self, id, init_state):
        super().__init__(id, init_state)

    def add_tetromino(self, tetromino):
        self.TETROMINOS.append(tetromino)

        base = tetromino.base_tile
        for tile in tetromino.tiles:
            self.BOARD[base[1] + tile[1]][base[0] +
                                          tile[0]] = self.tetromino_count
        self.tetromino_count += 1

    def move_tetromino(self, index, x, y):
        tetromino = self.TETROMINOS[index]
        for tile in tetromino.get_absolute_tiles():
            self.BOARD[tile[1]][tile[0]] = None
        tetromino.move(x, y)
        for tile in tetromino.get_absolute_tiles():
            self.BOARD[tile[1]][tile[0]] = index

    def update_state(self):
        pass

    def handle_event(self, event):
        pass

    def render(self, surface):

        # Draw the board
        pygame.draw.rect(surface, BOARD_COLOR, self.rect)

        # Draw the tetrominos
        for y in range(BOARD_HEIGHT_VISIBLE):
            for x in range(BOARD_WIDTH):
                if self.BOARD[y][x] is not None:
                    tetromino = self.TETROMINOS[self.BOARD[y][x]]
                    pygame.draw.rect(
                        surface, tetromino.color, self.RECTS[y][x])
                else:
                    pygame.draw.rect(
                        surface, BOARD_COLOR, self.RECTS[y][x], 1)
