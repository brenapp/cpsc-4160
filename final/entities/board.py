# board.py
#
# Author: Brendan McGuire
# Created 11 March 2023
#
# This entity represents the Tetris board in the game. Our implementation does not directly
# follow the Tetris Specification, but we take a lot of inspiration form it. The board is a 10x40
# grid of cells, but all cells above 20 are invisible.
#

import random
import entities.tetromino as tetromino
from . import entity
import pygame

# Represents the current state of the board. Each cell is either None (empty) or the index of
# the tetromino in the TETROMINOS array.
BOARD_WIDTH = 15
BOARD_HEIGHT = 25


class Board(entity.Entity):

    cells = [[None for x in range(BOARD_WIDTH)]
             for y in range(BOARD_HEIGHT)]

    tetrominos: list[tetromino.Tetromino] = []
    active_tetromino = None

    pieces = [
        (tetromino.I_PIECE, "CYAN"),
        (tetromino.J_PIECE, "BLUE"),
        (tetromino.L_PIECE, "ORANGE"),
        (tetromino.O_PIECE, "YELLOW"),
        (tetromino.S_PIECE, "GREEN"),
        (tetromino.Z_PIECE, "RED"),
        (tetromino.T_PIECE, "PURPLE")
    ]
    bag = []

    def __init__(self):
        self.add_piece()
        super().__init__()

    def add_piece(self):

        if len(self.bag) < 1:
            self.bag = list(range(len(self.pieces)))
            random.shuffle(self.bag)

        index = self.bag.pop()

        new_piece = self.pieces[index]
        self.add_tetromino(
            tetromino.Tetromino(0, (BOARD_WIDTH // 2, 1),
                                new_piece[0], new_piece[1])
        )

    def add_tetromino(self, tetromino: tetromino.Tetromino):
        self.active_tetromino = len(self.tetrominos)
        tetromino.index = self.active_tetromino
        self.tetrominos.append(tetromino)

        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = self.active_tetromino

    def move_active_tetromino(self, x, y):
        tetromino = self.tetrominos[self.active_tetromino]

        if not tetromino.can_move(x, y, self.cells):
            return

        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = None
        tetromino.move(x, y)
        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = self.active_tetromino

    def rotate_active_tetromino(self, direction):
        tetromino = self.tetrominos[self.active_tetromino]

        if not tetromino.can_rotate(direction, self.cells):
            return

        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = None
        tetromino.rotate(direction)
        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = self.active_tetromino

    def clear_lines(self):
        for y in range(BOARD_HEIGHT):
            if all([self.cells[y][x] is not None for x in range(BOARD_WIDTH)]):
                for x in range(BOARD_WIDTH):
                    self.cells[y][x] = None

                for y2 in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        self.cells[y2][x] = self.cells[y2 - 1][x]
