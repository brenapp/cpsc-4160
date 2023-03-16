import random
import pygame

I_PIECE = [(-1, 0), (0, 0), (1, 0), (2, 0)]
J_PIECE = [(-1, -1), (-1, 0), (0, 0), (1, 0)]
L_PIECE = [(-1, 0), (0, 0), (1, 0), (1, -1)]
O_PIECE = [(0, 0), (1, 0), (0, 1), (1, 1)]
S_PIECE = [(-1, 0), (0, 0), (0, 1), (1, 1)]
Z_PIECE = [(-1, 1), (-1, 0), (0, 0), (1, 0)]
T_PIECE = [(-1, 0), (0, 0), (1, 0), (0, 1)]

PIECES = [I_PIECE, J_PIECE, L_PIECE,  O_PIECE, S_PIECE, Z_PIECE, T_PIECE]

# Load the blocks
BLUE_BLOCK = pygame.image.load("assets/BlueBlock.png")
CYAN_BLOCK = pygame.image.load("assets/CyanBlock.png")
GREEN_BLOCK = pygame.image.load("assets/GreenBlock.png")
ORANGE_BLOCK = pygame.image.load("assets/OrangeBlock.png")
PURPLE_BLOCK = pygame.image.load("assets/PurpleBlock.png")
RED_BLOCK = pygame.image.load("assets/RedBlock.png")
YELLOW_BLOCK = pygame.image.load("assets/YellowBlock.png")

BLOCKS = [
    CYAN_BLOCK, BLUE_BLOCK, ORANGE_BLOCK, YELLOW_BLOCK, GREEN_BLOCK, RED_BLOCK, PURPLE_BLOCK
]


class Bag:

    tiles = [0, 1, 2, 3, 4, 5, 6]
    index = 0

    def __init__(self):
        random.shuffle(self.tiles)
        pass

    def get_next(self):
        tile = self.tiles[self.index]
        self.index += 1
        if self.index >= len(self.tiles):
            self.index = 0
            random.shuffle(self.tiles)
        return (PIECES[tile], BLOCKS[tile])
