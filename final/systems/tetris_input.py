import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.tetromino as tetromino
import entities.entity as entity
import entities.game_status as status
import pygame
import time


class TetrisInput(system.System):
    board: Board
    game_status: status.GameStatus
    last_move = time.time()
    last_player_move = time.time()

    def __init__(self, board, status: status.GameStatus):
        self.board = board
        self.hold = True
        self.game_status = status
        super().__init__()

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):
        # React to Keydown
        for event in events:
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

                if event.key == pygame.K_RSHIFT and self.hold:
                    self.board.hold_active_tetromino()
                    self.hold = False

        # React to held keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and time.time() - self.last_player_move > 0.05:
            if self.board.tetrominos[self.board.active_tetromino].can_move(
                0, 1, self.board.cells
            ):
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
        if (
            not active.can_move(0, 1, self.board.cells)
            and time.time() - self.last_player_move > 0.15
        ):
            self.board.clear_lines()

            self.board.add_piece()
            self.hold = True
            if not self.board.tetrominos[self.board.active_tetromino].can_move(
                0, 1, self.board.cells
            ):
                self.game_status.winner = status.Winner.FROG
                print("Game Status: Frog Wins")
