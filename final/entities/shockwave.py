import pygame

from entities.frog import ClampedValue
from . import entity

SHOCKWAVE_SIZE = 20


class Shockwave(entity.Entity):

    collider: pygame.Rect
    vel: tuple[ClampedValue, 2]

    def __init__(self, x, y):

        self.collider = pygame.Rect(x, y, SHOCKWAVE_SIZE, SHOCKWAVE_SIZE)
        self.vel = (
            ClampedValue(0, -10, 10),
            ClampedValue(0, -10, 10)
        )

        super().__init__()

    def step_kinematics(self):
        self.collider.x += self.vel[0].value
        self.collider.y += self.vel[1].value
