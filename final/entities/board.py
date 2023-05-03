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
import entities.tetromino
import entities.frog
from . import entity
import pygame

# Represents the current state of the board. Each cell is either None (empty) or the index of
# the tetromino in the TETROMINOS array.
BOARD_WIDTH = 15
BOARD_HEIGHT = 17


class Board(entity.Entity):

    cells: list[list[None | int]] = [[None for x in range(BOARD_WIDTH)]
                                     for y in range(BOARD_HEIGHT)]

    tetrominos: list[entities.tetromino.Tetromino] = []
    active_tetromino = None

    pieces = [
        (entities.tetromino.I_PIECE, "CYAN"),
        (entities.tetromino.J_PIECE, "BLUE"),
        (entities.tetromino.L_PIECE, "ORANGE"),
        (entities.tetromino.O_PIECE, "YELLOW"),
        (entities.tetromino.S_PIECE, "GREEN"),
        (entities.tetromino.Z_PIECE, "RED"),
        (entities.tetromino.T_PIECE, "PURPLE")
    ]
    bag = []

    held_piece = None

    def __init__(self):
        self.add_piece()
        super().__init__()

    def add_piece(self):

        if len(self.bag) < 2:
            new_order = list(range(len(self.pieces)))
            random.shuffle(new_order)
            self.bag.extend(new_order)

        index = self.bag.pop(0)

        new_piece = self.pieces[index]
        self.add_tetromino(
            entities.tetromino.Tetromino(0, (BOARD_WIDTH // 2, 1),
                                         new_piece[0], new_piece[1])
        )

    def add_tetromino(self, tetromino: entities.tetromino.Tetromino):
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

    def hold_active_tetromino(self):
        tetromino = self.tetrominos[self.active_tetromino]

        for tile in tetromino.get_absolute_tiles():
            self.cells[tile[1]][tile[0]] = None

        if self.held_piece is not None:
            self.add_tetromino(
                entities.tetromino.Tetromino(0, (BOARD_WIDTH // 2, 1),
                                             self.held_piece[0], self.held_piece[1])
            )
        else:
            self.add_piece()

        self.held_piece = (tetromino.tiles, tetromino.color)

    def clear_lines(self):
        for y in range(BOARD_HEIGHT):
            if all([self.cells[y][x] is not None for x in range(BOARD_WIDTH)]):
                for x in range(BOARD_WIDTH):
                    self.cells[y][x] = None

                for y2 in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        self.cells[y2][x] = self.cells[y2 - 1][x]
