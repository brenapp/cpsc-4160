import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import pygame
import time


class FrogInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    def __init__(self, board, frog):
        self.board = board
        self.frog = frog
        super().__init__()

    def run(self, entities):

        # React to Keydown
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # move the frog left
                if event.key == pygame.K_a:
                    self.frog.move(-1, 0)

                # move the frog right
                if event.key == pygame.K_d:
                    self.frog.move(1, 0)

        # React to held keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and time.time():
            self.frog.move(-1, 0)
        elif keys[pygame.K_d] and time.time():
            self.frog.move(1, 0)
