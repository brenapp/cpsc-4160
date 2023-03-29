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

        self.frog_collider.x = self.frog.pos[0].value
        self.frog_collider.y = self.frog.pos[1].value

        # Update the frog's position
        self.frog.step_kinematics()

        # check for y collisions
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board.cells[row][col] is not None:
                    collider = BOARD_TILE_RECTS[row][col]
                    if self.frog_collider.colliderect(collider):

                        # if we are on top
                        if self.frog_collider.bottom >= collider.top and self.frog_collider.bottom <= collider.bottom:
                            if self.frog.pos[1].value > collider.top - 30:
                                self.frog.pos[1].set(collider.top - 30)
                            if self.frog.vel[1].value > 0:
                                self.frog.vel[1].set(0)

                        # if we are on the bottom
                        if self.frog_collider.top <= collider.bottom and self.frog_collider.top >= collider.top:
                            if self.frog.pos[1].value < collider.bottom:
                                self.frog.pos[1].set(collider.bottom)
                            if self.frog.vel[1].value > 0:
                                self.frog.vel[1].set(0)

        # check for x collisions
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board.cells[row][col] is not None:
                    collider = BOARD_TILE_RECTS[row][col]
                    if self.frog_collider.colliderect(collider):

                        if self.frog_collider.right >= collider.left and self.frog_collider.right <= collider.right:
                            if self.frog.pos[0].value > collider.left - 30:
                                self.frog.pos[0].set(collider.left - 30)
                            if self.frog.vel[0].value > 0:
                                self.frog.vel[0].set(0)

                        if self.frog_collider.left <= collider.right and self.frog_collider.left >= collider.left:
                            if self.frog.pos[0].value < collider.right:
                                self.frog.pos[0].set(collider.right)
                            if self.frog.vel[0].value > 0:
                                self.frog.vel[0].set(0)
