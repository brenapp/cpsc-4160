import pygame
import entities.entity as entity
import entities.board as board
import entities.tetromino as tetromino
import entities.frog as frog
import entities.game_status as game_status
import systems.system as system
import systems.render_board as render_board
import systems.handle_shockwave as handle_shockwave
import systems.tetris_input as tetris_input
import systems.frog_input as frog_input
import systems.game_flow as game_flow
import systems.render_frog as render_frog
import systems.render_powerup as render_powerup

import sys

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

SCREEN_COLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption("Tetris Hopper")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Global Entities
status = game_status.GameStatus()
status.winner = game_status.Winner.NONE
game_board = board.Board()
game_frog = frog.Frog(game_board, 50, 50)


# Systems (run in this order)
tetris_input.TetrisInput(game_board, status)
frog_input.FrogInput(game_board, game_frog, status)

render_board.RenderTetrisBoard(game_board, surface)
render_frog.RenderFrog(game_board, game_frog, surface)
render_powerup.RenderPowerUp(game_board, surface)
handle_shockwave.HandleShockwave(game_board, surface)

game_flow.GameFlow(surface, status)


winner = None
while True:
    pygame.time.wait(10)

    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)

    if not status.game_over:
        surface.fill(SCREEN_COLOR)
        system.step_all(entity.ALL_ENTITIES)
        pygame.display.flip()
