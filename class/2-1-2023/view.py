import pygame
import sys

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SCREEN_COLOR = (255, 255, 255)
RECT_COLOR = (86, 50, 148)
RECT_SIZE = RECT_WIDTH, RECT_HEIGHT = (20, 20)

position = x_pos, y_pos = 100, 100

pygame.init()
pygame.display.set_caption("rectboi")
surface = pygame.display.set_mode(SCREEN_SIZE)


player_rect = pygame.Rect(x_pos, y_pos, RECT_WIDTH, RECT_HEIGHT)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.move_ip(-1, 0)
    elif keys[pygame.K_RIGHT] and player_rect.x < (SCREEN_WIDTH - player_rect.w):
        player_rect.move_ip(1, 0)
    elif keys[pygame.K_UP] and player_rect.y > 0:
        player_rect.move_ip(0, -1)
    elif keys[pygame.K_DOWN] and player_rect.y < (SCREEN_HEIGHT - player_rect.h):
        player_rect.move_ip(0, 1)
    elif keys[pygame.K_SPACE]:
        player_rect.w += 1
        player_rect.h += 1

    surface.fill(SCREEN_COLOR)
    pygame.draw.rect(surface, RECT_COLOR, player_rect)
    pygame.display.update()
