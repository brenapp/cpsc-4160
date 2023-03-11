import pygame
import sys
import entities.entity as entity
import entities.board as board

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810

SCREEN_COLOR = (0, 0, 0)

pygame.init()
pygame.display.set_caption("tetr")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


game_board = board.Board("board", {})
display = board.Tetromino(base_tile=(1, 1), tiles=[(
    0, 0), (1, 0), (2, 0), (3, 0)], color=(255, 0, 0))

game_board.add_tetromino(display)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    surface.fill(SCREEN_COLOR)
    entity.stepAll(surface)
    pygame.display.flip()
