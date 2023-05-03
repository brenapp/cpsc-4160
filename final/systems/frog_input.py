import sys

from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.frog as frog
import entities.entity as entity
import entities.game_status as status
from systems.render_board import BOARD_HEIGHT_PX, BOARD_WIDTH_PX, BOARD_X, BOARD_Y, BOARD_TILE_RECTS, BOARD_LEFT_WALL_RECT, BOARD_RIGHT_WALL_RECT, BOARD_BOTTOM_RECT, CELL_HEIGHT
import pygame
import time
from dataclasses import dataclass


@dataclass
class FrogStateGrounded:
    collider: pygame.Rect


@dataclass
class FrogStateAirborne:
    pass


FrogState = FrogStateGrounded | FrogStateAirborne


def sign(x):
    return (1 if x > 0 else -1)


class FrogInput(system.System):

    board: Board
    last_move = time.time()
    last_player_move = time.time()

    state: FrogState = FrogStateGrounded(collider=BOARD_BOTTOM_RECT)
    game_status: status.GameStatus

    def __init__(self, board: Board, frog: frog.Frog, status: status.GameStatus):
        self.board = board
        self.frog = frog
        self.game_status = status
        self.frog.direction = "right"
        self.frog.status = "idle"

        self.frog.vel[0].clamp(-10, 10)
        self.frog.vel[1].clamp(-10, 10)

        self.frog.collider.x = (BOARD_X + BOARD_WIDTH_PX / 2)
        self.frog.collider.y = (BOARD_HEIGHT_PX - 3 * CELL_HEIGHT)

        self.frog.step_kinematics()

        super().__init__()

    def get_collision_candidates(self):
        candidates = [BOARD_LEFT_WALL_RECT,
                      BOARD_RIGHT_WALL_RECT, BOARD_BOTTOM_RECT]
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                candidates.append(BOARD_TILE_RECTS[y][x])

        return candidates

    def colliding_any(self, candidates):
        for candidate in candidates:
            if self.frog.collider.colliderect(candidate):
                return candidate
        return None

    def side_colliding_any(self, candidates):
        for candidate in candidates:
            if self.frog.side_collider.colliderect(candidate):
                return candidate
        return None

    def check_if_falling(self, candidates):
        self.frog.collider.move_ip(0, 1)
        candidate = self.colliding_any(candidates)

        if candidate is not None:
            self.state = FrogStateGrounded(collider=candidate)
            self.frog.status = "idle"

        self.frog.collider.move_ip(0, -1)

    def check_collisions(self, offset, index, candidates):
        self.frog.collider.move_ip(offset)
        unaltered = True

        while self.frog.collider.collidelist(candidates) != -1:
            if index == 0:
                self.frog.collider.x -= sign(offset[index])
            else:
                self.frog.collider.y -= sign(offset[index])
            unaltered = False
        return unaltered

    def player_input(self):

        keys = pygame.key.get_pressed()

        self.frog.vel[0].set(0)

        if keys[pygame.K_a]:
            if isinstance(self.state, FrogStateGrounded):
                self.frog.vel[0].set(-3)
                self.frog.direction = "left"
                self.frog.status = "walking"
            else:
                self.frog.vel[0].set(-1)
                self.frog.direction = "left"

        elif keys[pygame.K_d]:
            if isinstance(self.state, FrogStateGrounded):
                self.frog.vel[0].set(3)
                self.frog.direction = "right"
                self.frog.status = "walking"
            else:
                self.frog.vel[0].set(1)
                self.frog.direction = "right"

        else:
            if isinstance(self.state, FrogStateGrounded):
                self.frog.status = "idle"

        if keys[pygame.K_w] and not isinstance(self.state, FrogStateAirborne):
            self.frog.vel[1].set(-3)
            self.state = FrogStateAirborne()
            self.frog.status = "airborne"

    def run(self, entities: list[entity.Entity], events: list[pygame.event.Event]):

        self.player_input()

        # Check collisions
        candidates = self.get_collision_candidates()
        side_candidates = self.get_collision_candidates()

        # Transitions

        match(self.state):

            case FrogStateGrounded(collider):

                # Jumping handled in player_input()
                self.frog.collider.move_ip(0, 1)

                colliding = self.colliding_any(candidates)
                if colliding is None:
                    self.state = FrogStateAirborne()
                    self.frog.status = "airborne"
                else:

                    # Get all rects colliding
                    colliding = self.frog.collider.collidelistall(candidates)

                    for i in colliding:

                        # if the frog is completely within the collision candidate, game over
                        overlap_horizontal = max(
                            0, min(self.frog.collider.right, candidates[i].right) - max(self.frog.collider.left, candidates[i].left))

                        within_vertical = (self.frog.collider.top >= candidates[i].top) and (
                            self.frog.collider.bottom <= candidates[i].bottom)

                        if within_vertical and overlap_horizontal > 10:
                            self.game_status.winner = status.Winner.TETRIS

                self.frog.collider.move_ip(0, -1)

            case FrogStateAirborne():

                self.frog.collider.move_ip((0, self.frog.vel[1].value))
                collision = self.colliding_any(candidates)

                altered = False

                while self.colliding_any(candidates) is not None:
                    self.frog.collider.move_ip(
                        0, -sign(self.frog.vel[1].value))
                    altered = True

                if altered:
                    self.state = FrogStateGrounded(collider=collision)
                    self.frog.status = "idle"

        if (self.frog.vel[0].value != 0):
            self.frog.collider.move_ip((self.frog.vel[0].value, 0))

            altered = False

            while self.colliding_any(candidates) is not None:
                self.frog.collider.move_ip(
                    -sign(self.frog.vel[0].value), 0)
                altered = True

            if altered:
                self.frog.vel[0].set(0)

        # Gravity
        if isinstance(self.state, FrogStateAirborne):
            self.frog.vel[1].set(min(1, self.frog.vel[1].value + 0.1))
        else:
            self.frog.vel[1].set(0)

        # Step physics
        self.frog.step_kinematics()

        if self.frog.collider.x < BOARD_X:
            self.frog.collider.x = BOARD_X

        if self.frog.collider.x > BOARD_X + BOARD_WIDTH_PX:
            self.frog.collider.x = BOARD_X + BOARD_WIDTH_PX

        if self.frog.collider.y < BOARD_Y:
            self.frog.collider.y = BOARD_Y

        if self.frog.collider.y > BOARD_Y + BOARD_HEIGHT_PX:
            self.frog.collider.y = BOARD_Y + BOARD_HEIGHT_PX

        self.frog.side_collider.x = self.frog.collider.x - 3
        self.frog.side_collider.y = self.frog.collider.y + 5

        # Side Testing
        i = self.side_colliding_any(candidates)

        if i is not None:
            # print("Side colliding")
            pass
