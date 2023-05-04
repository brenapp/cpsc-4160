from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
from entities.shockwave import Shockwave
from systems.render_board import BOARD_TILE_RECTS, BOARD_WIDTH_PX, BOARD_X
import systems.system as system
import pygame

IMAGES = {
    "SHOCKWAVE": pygame.image.load("assets/frog_attack.png"),
}

DRAW_HITBOXES = False


class HandleShockwave(system.System):

    surface: pygame.Surface
    board: Board

    def __init__(self, board, surface):
        self.surface = surface
        self.board = board

        self.image = IMAGES["SHOCKWAVE"]
        super().__init__()

    def run(self, entities, events):

        shockwaves: list[Shockwave] = [
            e for e in entities if e.__class__.__name__ == "Shockwave"]

        candidates: list[tuple[int, int, pygame.Rect]] = []
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                candidates.append((x, y, BOARD_TILE_RECTS[y][x]))

        for shockwave in shockwaves:
            shockwave.step_kinematics()

            rects = [c[2] for c in candidates]
            collides = shockwave.collider.collidelistall(rects)

            if shockwave.collider.x < BOARD_X or shockwave.collider.x > BOARD_X + BOARD_WIDTH_PX:
                shockwave.remove()
                continue

            if len(collides) > 0:
                remove = candidates[collides[0]]
                self.board.cells[remove[1]][remove[0]] = None

                shockwave.remove()

            if shockwave.vel[0].value > 0:
                self.surface.blit(self.image, shockwave.collider)
            else:
                self.surface.blit(pygame.transform.flip(
                    self.image, True, False), shockwave.collider)
