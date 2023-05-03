from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import pygame

IMAGES = {
    "SHOCKWAVE": pygame.image.load("assets/frog_attack.png"),
}

DRAW_HITBOXES = False


class HandleShockwave(system.System):

    surface: pygame.Surface
    board: Board

    def __init__(self, surface):
        self.surface = surface
        self.airtime = 0
        self.walktime = 0
        self.image = IMAGES["SHOCKWAVE"]
        super().__init__()

    def run(self, entities, events):

        shockwaves = [
            e for e in entities if e.__class__.__name__ == "Shockwave"]

        for shockwave in shockwaves:
            shockwave.step_kinematics()

            if shockwave.vel[0].value > 0:
                self.surface.blit(self.image, shockwave.collider)
            else:
                self.surface.blit(pygame.transform.flip(
                    self.image, True, False), shockwave.collider)
