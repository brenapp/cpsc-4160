from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.entity as entity
import entities.frog as frog
import pygame


class RenderPowerUp(system.System):

    surface: pygame.Surface
    board: Board

    def __init__(self, board, surface):
        self.surface = surface
        self.board = board

        super().__init__()

    def run(self, entities, events):
        powerups = entity.get_all_entities_by_type("PowerUp")
