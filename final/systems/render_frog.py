from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.entity as entity
import entities.frog as frog
import pygame

IMAGES = {
    "FROG": pygame.image.load("assets/frog.png")
}


class RenderFrog(system.System):

    surface: pygame.Surface
    board: Board
    frog: frog.Frog

    def __init__(self, board, frog, surface):
        self.surface = surface
        self.board = board
        self.frog = frog
        super().__init__()

    def run(self, entities, events):

        # Draw the frog
        pygame.Surface.blit(
            self.surface, IMAGES["FROG"], (self.frog.collider.x, self.frog.collider.y - 10))
