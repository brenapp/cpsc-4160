import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import entities.entity as entity
from systems.render_board import BOARD_HEIGHT_PX, BOARD_WIDTH_PX, BOARD_X, BOARD_Y, BOARD_TILE_RECTS, BOARD_LEFT_WALL_RECT, BOARD_RIGHT_WALL_RECT, BOARD_BOTTOM_RECT
import pygame
import time
import itertools
from dataclasses import dataclass


@dataclass
class FrogStateGrounded:
    collider: pygame.Rect


@dataclass
class FrogStateAirborne:
    pass


@dataclass
class FrogStateClinging:
    collider: pygame.Rect


FrogState = FrogStateGrounded | FrogStateAirborne | FrogStateClinging


class FrogInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    frog_collider: pygame.Rect
    state: FrogState = FrogStateGrounded(collider=BOARD_BOTTOM_RECT)

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

    def run_x(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_a] and not isinstance(self.state, FrogStateClinging):
            self.frog.apply_force(-2, 0)
        elif keys[pygame.K_d] and not isinstance(self.state, FrogStateClinging):
            self.frog.apply_force(2, 0)

        # Friction in the x direction
        self.frog.apply_force(-1 * self.frog.vel[0].value, 0)

        self.frog.step_kinematics_x()
        self.frog_collider.x = self.frog.pos[0].value

        # Check for collisions with the board
        colliding = False
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                if self.frog_collider.colliderect(BOARD_TILE_RECTS[y][x]):
                    if self.frog.vel[0].value > 0:
                        self.frog.pos[0].set(BOARD_TILE_RECTS[y][x].x - 30)
                    elif self.frog.vel[0].value < 0:
                        self.frog.pos[0].set(BOARD_TILE_RECTS[y][x].x + 30)

                    if isinstance(self.state, FrogStateAirborne):
                        self.state = FrogStateClinging(
                            collider=BOARD_TILE_RECTS[y][x])

                    colliding = True

                    self.frog.vel[0].set(0)
                    self.frog.acc[0].set(0)

        if not colliding and isinstance(self.state, FrogStateClinging):
            self.state = FrogStateAirborne()

    def run_y(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        # Game defined state collisions
        colliding = False
        match self.state:
            case FrogStateGrounded(collider):
                pass
            case FrogStateAirborne():
                if self.frog_collider.colliderect(BOARD_BOTTOM_RECT):
                    self.state = FrogStateGrounded(collider=BOARD_BOTTOM_RECT)
                    self.frog.pos[1].set(BOARD_BOTTOM_RECT.y - 30)
            case FrogStateClinging(collider):
                pass

        # Player Defined Transitions
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and isinstance(self.state, FrogStateGrounded):
                    self.state = FrogStateAirborne()
                    self.frog.vel[1].set(0)
                    self.frog.apply_force(0, -5)

        # Only apply gravity when you're airborne
        if isinstance(self.state, FrogStateAirborne):
            self.frog.apply_force(0, 0.1)
            self.frog.vel[1].clamp(-5, 5)

        # Apply gravity when you're clinging
        if isinstance(self.state, FrogStateClinging):
            self.frog.apply_force(0, 0.1)
            self.frog.vel[1].clamp(0, 0.3)

        if isinstance(self.state, FrogStateGrounded):
            self.frog.vel[1].set(0)
            self.frog.acc[1].set(0)

        self.frog.step_kinematics_y()
        self.frog_collider.y = self.frog.pos[1].value

        # Check for collisions with the board

        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                if self.frog_collider.colliderect(BOARD_TILE_RECTS[y][x]):
                    if self.frog.vel[1].value > 0:
                        self.frog.pos[1].set(BOARD_TILE_RECTS[y][x].y - 30)
                    elif self.frog.vel[1].value < 0:
                        self.frog.pos[1].set(BOARD_TILE_RECTS[y][x].y + 30)

                    if isinstance(self.state, FrogStateAirborne):
                        self.state = FrogStateGrounded(
                            collider=BOARD_TILE_RECTS[y][x])

                    colliding = True

                    self.frog.vel[1].set(0)
                    self.frog.acc[1].set(0)

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):
        self.run_x(entities=entities, events=events)
        self.run_y(entities=entities, events=events)
        print(self.state)
