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
            pygame.draw.rect(self.surface, (255, 255, 255),
                             pygame.Rect(0, CELL_HEIGHT * 4, 900, CELL_HEIGHT * 4))

            text_surface = self.font.render(
                "GAME OVER", True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(900 // 2, CELL_HEIGHT * 5))
            self.surface.blit(text_surface, text_rect)

            winner = "FROG" if self.game_status.winner == status.Winner.FROG else "TETRIS"
            text_surface = self.font.render(
                "WINNER: " + winner, True, "Coral" if self.game_status.winner == status.Winner.FROG else "Blue")
            text_rect = text_surface.get_rect(
                center=(900 // 2, CELL_HEIGHT * 7))
            self.surface.blit(text_surface, text_rect)

            pygame.display.flip()
            self.game_status.game_over = True
