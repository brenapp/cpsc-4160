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

import entity
import pygame


class Board(entity.Entity):

    def __init__(self, id, init_state):
        super().__init__(id, init_state)
