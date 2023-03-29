import pygame
import entities.entity as entity
import entities.board as board
import entities.tetromino as tetromino
import entities.frog as frog
import systems.system as system
import systems.render_board as render_board
import systems.tetris_input as tetris_input
import systems.frog_input as frog_input
import systems.render_frog as render_frog

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
tetris_input.TetrisInput(game_board)

game_frog = frog.Frog(game_board, 50, 50)
render_frog.RenderFrog(game_board, game_frog, surface)
frog_input.FrogInput(game_board, game_frog)


while True:
    pygame.time.wait(10)

    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    surface.fill(SCREEN_COLOR)
    system.step_all(entity.ALL_ENTITIES)
    pygame.display.flip()
