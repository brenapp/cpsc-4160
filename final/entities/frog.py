import pygame
from . import entity


class ClampedValue:

    def __init__(self, value, min_value, max_value):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def set(self, value):
        self.value = max(self.min_value, min(self.max_value, value))

    def add(self, value):
        self.set(self.value + value)

    def clamp(self, min, max):
        self.min_value = min
        self.max_value = max

    def is_clamped(self):
        return self.value == self.min_value or self.value == self.max_value

    def __repr__(self):
        return f"ClampedValue({self.value}, {self.min_value}, {self.max_value})"


class Frog(entity.Entity):

    vel: tuple[ClampedValue, 2]

    def __init__(self, board, pos_x, pos_y):

        self.vel = (
            ClampedValue(0, 0, 0),
            ClampedValue(0, 0, 0)
        )

        self.direction = "right"
        self.status = "idle"

        self.collider = pygame.Rect(0, 0, 20, 20)

    def step_kinematics(self):
        self.collider.x += self.vel[0].value
        self.collider.y += self.vel[1].value
