import pygame
import entities.entity as entity
import entities.board as board
import entities.tetromino as tetromino
import systems.system as system
import systems.render_board as render_board
import sys

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810

SCREEN_COLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption("tetris platform")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_board = board.Board()
render_board.RenderTetrisBoard(game_board, surface)

init = tetromino.Tetromino(0, (1, 1), tetromino.J_PIECE, "RED")
game_board.add_tetromino(init)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                game_board.move_active_tetromino(-1, 0)

            if event.key == pygame.K_RIGHT:
                game_board.move_active_tetromino(1, 0)

    pygame.time.wait(10)

    surface.fill(SCREEN_COLOR)
    system.step_all(entity.ALL_ENTITIES)
    pygame.display.flip()
