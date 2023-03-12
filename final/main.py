import pygame
import sys
import entities.entity as entity
import entities.board as board
import time
import random
import bag

# Screen Dimensions (1920x1080 scaled to 75%)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 810

SCREEN_COLOR = (30, 30, 30)

pygame.init()
pygame.display.set_caption("tetr")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_board = board.Board("board", {})


piece_bag = bag.Bag()
tiles, color = piece_bag.get_next()
game_board.add_tetromino((1, 1), tiles, color)

last_player_move = time.time()
last_move_down = time.time()
active_tetromino = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[pygame.K_DOWN] and time.time() - last_player_move > 0.05:
        game_board.move_tetromino(active_tetromino, 0, 1)
        last_player_move = time.time()

    if pygame.key.get_pressed()[pygame.K_LEFT] and time.time() - last_player_move > 0.10:
        game_board.move_tetromino(active_tetromino, -1, 0)
        last_player_move = time.time()

    if pygame.key.get_pressed()[pygame.K_RIGHT] and time.time() - last_player_move > 0.10:
        game_board.move_tetromino(active_tetromino, 1, 0)
        last_player_move = time.time()

    if pygame.key.get_pressed()[pygame.K_UP] and time.time() - last_player_move > 0.10:
        game_board.rotate_tetromino(active_tetromino, "ccw")
        last_player_move = time.time()

    if time.time() - last_move_down > 0.5 and last_player_move > 0.05:
        game_board.move_tetromino(active_tetromino, 0, 1)
        last_move_down = time.time()

    # if the active tetromino can't move down, create a new one
    if not game_board.tetromino_is_active(active_tetromino) and time.time() - last_move_down > 0.25:
        tiles, color = piece_bag.get_next()
        game_board.add_tetromino((1, 1), tiles, color)
        active_tetromino += 1
        last_move_down = time.time()

    surface.fill(SCREEN_COLOR)
    entity.stepAll(surface)
    pygame.display.flip()
