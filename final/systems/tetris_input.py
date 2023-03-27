import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.tetromino as tetromino
import pygame
import time
import random


class TetrisInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    def __init__(self, board):
        self.board = board
        super().__init__()

    def run(self, entities):

        # React to Keydown
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # move the active tetromino left
                if event.key == pygame.K_LEFT:
                    self.board.move_active_tetromino(-1, 0)
                    self.last_player_move = time.time()

                # move the active tetromino right
                if event.key == pygame.K_RIGHT:
                    self.board.move_active_tetromino(1, 0)
                    self.last_player_move = time.time()

                # rotate the active tetromino
                if event.key == pygame.K_UP:
                    self.board.rotate_active_tetromino("ccw")
                    self.last_player_move = time.time()

        # React to held keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and time.time() - self.last_player_move > 0.05:
            self.board.move_active_tetromino(0, 1)
            self.last_player_move = time.time()
        elif keys[pygame.K_LEFT] and time.time() - self.last_player_move > 0.15:
            self.board.move_active_tetromino(-1, 0)
            self.last_player_move = time.time()
        elif keys[pygame.K_RIGHT] and time.time() - self.last_player_move > 0.15:
            self.board.move_active_tetromino(1, 0)
            self.last_player_move = time.time()
        elif keys[pygame.K_UP] and time.time() - self.last_player_move > 0.15:
            self.board.rotate_active_tetromino("cw")
            self.last_player_move = time.time()

        # Move the active tetromino down
        if time.time() - self.last_move > 0.5:
            self.board.move_active_tetromino(0, 1)
            self.last_move = time.time()

        # Spawn new tetromino if we can't move the current one down
        active = self.board.tetrominos[self.board.active_tetromino]
        if not active.can_move(0, 1, self.board.cells) and time.time() - self.last_player_move > 0.15:
            self.board.clear_lines()

            self.board.add_piece()
            if not self.board.tetrominos[self.board.active_tetromino].can_move(0, 1, self.board.cells):
                print("Game Over!")
                sys.exit()
