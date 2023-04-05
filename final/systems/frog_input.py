import sys
from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import entities.entity as entity
from systems.render_board import BOARD_HEIGHT_PX, BOARD_WIDTH_PX, BOARD_X, BOARD_Y, BOARD_TILE_RECTS, BOARD_LEFT_WALL_RECT, BOARD_RIGHT_WALL_RECT, BOARD_BOTTOM_RECT, CELL_HEIGHT
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

        if keys[pygame.K_a]:
            self.frog.apply_force(-5, 0)

        if keys[pygame.K_d]:
            self.frog.apply_force(5, 0)

          # Colliding with the candidates
        self.frog.pos[0].clamp(BOARD_X, BOARD_WIDTH_PX)
        candidates = [BOARD_LEFT_WALL_RECT, BOARD_RIGHT_WALL_RECT]
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                if isinstance(self.state, FrogStateGrounded) and (y * CELL_HEIGHT) >= self.frog.pos[1].value:
                    continue

                candidates.append(BOARD_TILE_RECTS[y][x])

        for candidate in candidates:
            if self.frog_collider.colliderect(candidate):

                if self.frog.vel[0].value > 0:
                    self.frog.pos[0].max_value = candidate.left
                elif self.frog.vel[0].value < 0:
                    self.frog.pos[0].min_value = candidate.right

                break

        # Apply Forces
        self.frog.apply_force(-1 * self.frog.vel[0].value, 0)

        # Step Kinematics
        self.frog.step_kinematics_x()
        self.frog_collider.x = self.frog.pos[0].value

    def run_y(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        # Transitions Between States
        keys = pygame.key.get_pressed()
        match self.state:
            case FrogStateGrounded(collider):

                if not self.frog_collider.colliderect(collider):
                    self.state = FrogStateAirborne()

                if keys[pygame.K_SPACE]:
                    self.frog.apply_force(0, -20)
                    self.state = FrogStateAirborne()

            case FrogStateAirborne():

                # Colliding with the candidates
                candidates = [BOARD_BOTTOM_RECT]
                for y in range(0, BOARD_HEIGHT):
                    for x in range(0, BOARD_WIDTH):
                        if self.board.cells[y][x] is None:
                            continue

                        candidates.append(BOARD_TILE_RECTS[y][x])

                for candidate in candidates:
                    if self.frog_collider.colliderect(candidate):
                        self.state = FrogStateGrounded(collider=candidate)
                        break

                pass
            case FrogStateClinging(collider):
                pass

        # Apply Forces

        # Gravity
        if isinstance(self.state, FrogStateAirborne):
            self.frog.apply_force(0, 0.1)
            self.frog.vel[1].clamp(-5, 5)
        elif isinstance(self.state, FrogStateClinging):
            self.frog.apply_force(0, 0.1)
            self.frog.vel[1].clamp(0, 0.3)
        else:
            self.frog.vel[1].set(0)
            self.frog.acc[1].set(0)

        # Step Kinematics
        self.frog.step_kinematics_y()
        self.frog_collider.y = self.frog.pos[1].value

        print(self.state)

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):
        self.run_x(entities=entities, events=events)
        self.run_y(entities=entities, events=events)
