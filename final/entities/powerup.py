import pygame
from . import entity
from dataclasses import dataclass


class PowerUp(entity.Entity):

    collider: pygame.Rect

    def __init__(self, pos_x, pos_y):
        self.collider = pygame.Rect(pos_x, pos_y, 20, 20)
