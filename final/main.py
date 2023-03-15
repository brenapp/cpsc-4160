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
tiles, image = piece_bag.get_next()
game_board.add_tetromino((1, 1), tiles, image)

last_move = time.time()
last_player_move = time.time()
active_tetromino = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # move the active tetromino left
            if event.key == pygame.K_LEFT:
                game_board.move_tetromino(active_tetromino, -1, 0)
                last_player_move = time.time()

            # move the active tetromino right
            if event.key == pygame.K_RIGHT:
                game_board.move_tetromino(active_tetromino, 1, 0)
                last_player_move = time.time()

            # rotate the active tetromino
            if event.key == pygame.K_UP:
                game_board.rotate_tetromino(active_tetromino, "ccw")
                last_player_move = time.time()

    # Hold to move
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN] and time.time() - last_player_move > 0.05:
        game_board.move_tetromino(active_tetromino, 0, 1)
        last_player_move = time.time()
    elif keys[pygame.K_LEFT] and time.time() - last_player_move > 0.15:
        game_board.move_tetromino(active_tetromino, -1, 0)
        last_player_move = time.time()
    elif keys[pygame.K_RIGHT] and time.time() - last_player_move > 0.15:
        game_board.move_tetromino(active_tetromino, 1, 0)
        last_player_move = time.time()
    elif keys[pygame.K_UP] and time.time() - last_player_move > 0.15:
        game_board.rotate_tetromino(active_tetromino, "cw")

    # move the active tetromino down
    if time.time() - last_move > 0.15:
        if game_board.tetromino_is_active(active_tetromino):
            game_board.move_tetromino(active_tetromino, 0, 1)
        last_move = time.time()

    # if the active tetromino can't move down, create a new one
    if not game_board.tetromino_is_active(active_tetromino) and time.time() - last_player_move > 0.5:

        # Clear filled lines
        game_board.clear_lines()

        tiles, image = piece_bag.get_next()
        game_board.add_tetromino((board.BOARD_WIDTH // 2, 1), tiles, image)
        active_tetromino += 1
        last_move = time.time()

        # Check if game over
        if not game_board.tetromino_is_active(active_tetromino):
            print("Game Over")
            pygame.quit()
            sys.exit()


    surface.fill(SCREEN_COLOR)
    entity.stepAll(surface)
    pygame.display.flip()
