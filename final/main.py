import pygame
import sys
import entities.entity as entity
import entities.board as board
import time

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810

SCREEN_COLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption("tetr")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_board = board.Board("board", {})


game_board.add_tetromino(base_tile=(1, 1), tiles=[(
    0, 0), (1, 0), (2, 0), (3, 0)], color=(255, 0, 0))

last_move = time.time()
active_tetromino = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[pygame.K_DOWN] and time.time() - last_move > 0.05:
        game_board.move_tetromino(active_tetromino, 0, 1)
        last_move = time.time()

    # move the tetromino down every 0.5 seconds
    if time.time() - last_move > 0.5:

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            game_board.move_tetromino(active_tetromino, -1, 0)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            game_board.move_tetromino(active_tetromino, 1, 0)

        if pygame.key.get_pressed()[pygame.K_UP]:
            game_board.rotate_tetromino(active_tetromino, "cw")

        game_board.move_tetromino(active_tetromino, 0, 1)
        last_move = time.time()

    # if the active tetromino can't move down, create a new one
    if not game_board.tetromino_is_active(active_tetromino):
        game_board.add_tetromino(base_tile=(1, 1), tiles=[(
            0, 0), (1, 0), (2, 0), (3, 0)], color=(255, 0, 0))
        active_tetromino += 1

    surface.fill(SCREEN_COLOR)
    entity.stepAll(surface)
    pygame.display.flip()
