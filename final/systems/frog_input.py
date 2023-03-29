import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import entities.entity as entity
from systems.render_board import BOARD_HEIGHT_PX, BOARD_WIDTH_PX, BOARD_X, BOARD_Y, BOARD_TILE_RECTS
import pygame
import time


class FrogInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    frog_collider: pygame.Rect
    move_state = "on_ground"  # "on_ground", "in_air"

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
        self.frog.pos[1].set(BOARD_HEIGHT_PX)

        self.frog.vel[0].set(0)
        self.frog.vel[1].set(0)

        self.frog.acc[0].set(0)
        self.frog.acc[1].set(0)

        self.frog_collider = pygame.Rect(
            self.frog.pos[0].value, self.frog.pos[1].value, 30, 30)

        super().__init__()

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_a] and time.time():
            self.frog.apply_force(-2, 0)
        elif keys[pygame.K_d] and time.time():
            self.frog.apply_force(2, 0)

        # Friction in the x direction
        self.frog.apply_force(-1 * self.frog.vel[0].value, 0)

        self.frog.step_kinematics_x()
        self.frog_collider.x = self.frog.pos[0].value

        # check for horizontal collisions
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board.cells[row][col] is not None:
                    collider = BOARD_TILE_RECTS[row][col]
                    if self.frog_collider.colliderect(collider):

                        if self.frog.vel[0].value < 0:
                            self.frog.pos[0].set(collider.right)
                            self.frog.vel[0].set(0)
                        elif self.frog.vel[0].value > 0:
                            self.frog.pos[0].set(collider.left - 30)
                            self.frog.vel[0].set(0)

        # Vertical Movement
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.frog.pos[1].value == BOARD_HEIGHT_PX:
                    self.frog.vel[1].set(0)
                    self.frog.apply_force(0, -5)

        # Gravity
        if self.frog.pos[1].value < BOARD_HEIGHT_PX:
            self.frog.apply_force(0, 0.1)

        self.frog.step_kinematics_y()
        self.frog_collider.y = self.frog.pos[1].value

        # check for horizontal collisions
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board.cells[row][col] is not None:
                    collider = BOARD_TILE_RECTS[row][col]
                    if self.frog_collider.colliderect(collider):

                        if self.frog.vel[1].value > 0:
                            self.frog.pos[1].set(collider.top - 30)
                            self.frog.vel[1].set(0)

                        elif self.frog.vel[1].value < 0:
                            self.frog.pos[1].set(collider.bottom)
