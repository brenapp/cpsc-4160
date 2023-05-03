import pygame
from . import entity
from enum import Enum

Winner = Enum("Winner", ["FROG", "TETRIS", "NONE"])


class GameStatus(entity.Entity):

    winner: Winner = Winner.NONE
    game_over = False
