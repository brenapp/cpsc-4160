import pygame
import entities.entity as entity
import entities.board as board
import entities.tetromino as tetromino
import entities.frog as frog
import entities.powerup as powerup
import systems.system as system
import systems.render_board as render_board
import systems.input_tetris as input_tetris
import systems.input_frog as input_frog
import systems.render_frog as render_frog
import systems.render_powerup as render_powerup

import sys

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

SCREEN_COLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption("tetris platform")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game_board = board.Board()
render_board.RenderTetrisBoard(game_board, surface)
input_tetris.TetrisInput(game_board)

game_frog = frog.Frog(game_board, 50, 50)
render_frog.RenderFrog(game_board, game_frog, surface)
input_frog.FrogInput(game_board, game_frog)


render_powerup.RenderPowerUp(game_board, surface)

game_powerup = powerup.PowerUp(0, 0)

while True:
    pygame.time.wait(10)

    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    surface.fill(SCREEN_COLOR)
    system.step_all(entity.ALL_ENTITIES)
    pygame.display.flip()
