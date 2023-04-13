from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.entity as entity
import entities.frog as frog
import pygame

IMAGES = {
    "FROG": pygame.image.load("assets/frog.png"),
    "FROG_IDLE1": pygame.image.load("assets/frog_idle1.png"),
    "FROG_IDLE2": pygame.image.load("assets/frog_idle2.png"),
    "FROG_IDLE3": pygame.image.load("assets/frog_idle3.png"),
    "FROG_IDLE4": pygame.image.load("assets/frog_idle4.png"),
    "FROG_IDLE5": pygame.image.load("assets/frog_idle5.png"),
}


class RenderFrog(system.System):

    surface: pygame.Surface
    board: Board
    frog: frog.Frog

    def __init__(self, board, frog, surface):
        self.surface = surface
        self.board = board
        self.frog = frog
        self.image = IMAGES["FROG"]
        self.status = "idle"
        self.facing = "right"
        super().__init__()

    def run(self, entities, events):

        # Draw the frog
        frameNum = pygame.time.get_ticks()
        idletime = frameNum % 600
        if (self.status == "idle"):
            if (idletime >= 0 and idletime < 100):
                self.image = IMAGES["FROG"]
            if (idletime >= 100 and idletime < 200):
                self.image = IMAGES["FROG_IDLE1"]
            if (idletime >= 200 and idletime < 300):
                self.image = IMAGES["FROG_IDLE2"]
            if (idletime >= 300 and idletime < 400):
                self.image = IMAGES["FROG_IDLE3"]
            if (idletime >= 400 and idletime < 500):
                self.image = IMAGES["FROG_IDLE4"]
            if (idletime >= 500 and idletime < 600):
                self.image = IMAGES["FROG_IDLE5"]

        if (self.facing == "left"):
            pygame.Surface.blit(self.surface, pygame.transform.flip(self.image, True, False),
                                (self.frog.collider.x, self.frog.collider.y))
        elif (self.facing == "right"):
            pygame.Surface.blit(
                self.surface, self.image, (self.frog.collider.x, self.frog.collider.y - 10))
