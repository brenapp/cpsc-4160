import entities.game_status as status
from systems.render_board import BOARD_WIDTH_PX, CELL_HEIGHT
import systems.system as system
import entities.entity as entity
import entities.frog as frog
import pygame


class GameFlow(system.System):

    surface: pygame.Surface
    game_status: status.GameStatus
    font: pygame.font.Font

    def __init__(self, surface, status):
        self.surface = surface
        self.game_status = status
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

        super().__init__()

    def run(self, entities, events):

        if self.game_status.winner != status.Winner.NONE:
            if self.game_status.winner == status.Winner.FROG:
                self.surface.blit(pygame.image.load(
                    "assets/frog_win.png"), (0, 0))
            else:
                self.surface.blit(pygame.image.load(
                    "assets/tetris_win.png"), (0, 0))

            pygame.display.flip()
            self.game_status.game_over = True
