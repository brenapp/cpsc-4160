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
    "FROG_JUMP1": pygame.image.load("assets/frog_jump1.png"),
    "FROG_JUMP2": pygame.image.load("assets/frog_jump2.png"),
    "FROG_JUMP3": pygame.image.load("assets/frog_jump3.png"),
    "FROG_JUMP4": pygame.image.load("assets/frog_jump4.png"),
    "FROG_JUMP5": pygame.image.load("assets/frog_jump5.png"),
    "FROG_JUMP6": pygame.image.load("assets/frog_jump6.png"),
}

DRAW_HITBOXES = False


class RenderFrog(system.System):

    surface: pygame.Surface
    board: Board
    frog: frog.Frog

    def __init__(self, board, frog, surface):
        self.surface = surface
        self.board = board
        self.frog = frog
        self.airtime = 0
        self.image = IMAGES["FROG"]
        super().__init__()

    def run(self, entities, events):

        # Draw the frog
        frameNum = pygame.time.get_ticks()
        idletime = frameNum % 600
        if (self.frog.status != "airborne"):
            self.airtime = 0
        if (self.frog.status == "idle"):
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

        if (self.frog.status == "airborne"):
            if (self.airtime >= 0 and self.airtime < 1):
                self.image = IMAGES["FROG"]
            if (self.airtime >= 1 and self.airtime < 3):
                self.image = IMAGES["FROG_JUMP1"]
            if (self.airtime >= 3 and self.airtime < 6):
                self.image = IMAGES["FROG_JUMP2"]
            if (self.airtime >= 6 and self.airtime < 9):
                self.image = IMAGES["FROG_JUMP3"]
            if (self.airtime >= 9 and self.airtime < 12):
                self.image = IMAGES["FROG_JUMP4"]
            if (self.airtime >= 12 and self.airtime < 15):
                self.image = IMAGES["FROG_JUMP5"]
            if (self.airtime >= 15):
                self.image = IMAGES["FROG_JUMP6"]
            self.airtime += 1

        if (self.frog.direction == "left"):
            pygame.Surface.blit(self.surface, pygame.transform.flip(self.image, True, False),
                                (self.frog.collider.x, self.frog.collider.y - 10))
        elif (self.frog.direction == "right"):
            pygame.Surface.blit(
                self.surface, self.image, (self.frog.collider.x, self.frog.collider.y - 10))

        # Draw hitboxes
        red = (255, 0, 0)
        green = (0, 255, 0)

        if DRAW_HITBOXES:
            pygame.draw.rect(self.surface, red, self.frog.collider)
            pygame.draw.rect(self.surface, green, self.frog.side_collider)
