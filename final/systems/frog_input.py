import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import entities.entity as entity
from systems.render_board import BOARD_HEIGHT_PX, BOARD_WIDTH_PX, BOARD_X, BOARD_Y
import pygame
import time


class FrogInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    def __init__(self, board: Board, frog: frog.Frog):
        self.board = board
        self.frog = frog

        self.frog.pos[0].clamp(BOARD_X, BOARD_WIDTH_PX)
        self.frog.pos[1].clamp(BOARD_Y, BOARD_HEIGHT_PX)

        self.frog.vel[0].clamp(-5, 5)
        self.frog.vel[1].clamp(-5, 5)

        self.frog.acc[0].clamp(-5, 5)
        self.frog.acc[1].clamp(-5, 5)

        self.frog.pos[0].set(BOARD_X + BOARD_WIDTH_PX / 2)
        self.frog.pos[1].set(BOARD_Y)

        self.frog.vel[0].set(0)
        self.frog.vel[1].set(0)

        self.frog.acc[0].set(0)
        self.frog.acc[1].set(0)

        super().__init__()

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.frog.pos[1].value == BOARD_HEIGHT_PX:
                    self.frog.vel[1].set(0)
                    self.frog.apply_force(0, -5)

        # React to held keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and time.time():
            self.frog.apply_force(-2, 0)
        elif keys[pygame.K_d] and time.time():
            self.frog.apply_force(2, 0)

        # Friction in the x direction
        self.frog.apply_force(-1 * self.frog.vel[0].value, 0)

        # Gravity
        if self.frog.pos[1].value < BOARD_HEIGHT_PX:
            self.frog.apply_force(0, 0.1)

        print(self.frog.pos[1], self.frog.vel[1], self.frog.acc[1])

        # Update the frog's position
        self.frog.step_kinematics()
