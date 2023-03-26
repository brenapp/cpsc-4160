from entities.board import Board, BOARD_WIDTH, BOARD_HEIGHT
import systems.system as system
import entities.entity as entity
import pygame


CELL_WIDTH = 30
CELL_HEIGHT = 30

BOARD_WIDTH_PX = CELL_WIDTH * BOARD_WIDTH
BOARD_HEIGHT_PX = CELL_HEIGHT * BOARD_HEIGHT
BOARD_X = CELL_WIDTH
BOARD_Y = CELL_HEIGHT
BOARD_COLOR = (255, 255, 255)
GRID_LINE_COLOR = (200, 200, 200)

BOARD_RECT = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH_PX, BOARD_HEIGHT_PX)
BOARD_TILE_RECTS = [[pygame.Rect(BOARD_X + x * CELL_WIDTH, BOARD_Y + y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                     for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

IMAGES = {
    "BLUE": pygame.image.load("assets/BlueBlock.png"),
    "CYAN": pygame.image.load("assets/CyanBlock.png"),
    "GREEN": pygame.image.load("assets/GreenBlock.png"),
    "ORANGE":  pygame.image.load("assets/OrangeBlock.png"),
    "PURPLE": pygame.image.load("assets/PurpleBlock.png"),
    "RED": pygame.image.load("assets/RedBlock.png"),
    "YELLOW": pygame.image.load("assets/YellowBlock.png"),
}


class RenderTetrisBoard(system.System):

    surface: pygame.Surface
    board: Board

    def __init__(self, board, surface):
        self.surface = surface
        self.board = board
        super().__init__()

    def run(self, entities):
        # Draw the board
        pygame.draw.rect(self.surface, BOARD_COLOR, BOARD_RECT)

        # Draw grid lines
        for x in range(BOARD_WIDTH):
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (BOARD_X + x *
                             CELL_WIDTH, BOARD_Y), (BOARD_X + x * CELL_WIDTH, BOARD_Y + BOARD_HEIGHT_PX))

        for y in range(BOARD_HEIGHT):
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (BOARD_X,
                             BOARD_Y + y * CELL_HEIGHT), (BOARD_X + BOARD_WIDTH_PX, BOARD_Y + y * CELL_HEIGHT))

        # Draw the tetrominos
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board.cells[y][x] is not None:
                    tetromino = self.board.tetrominos[self.board.cells[y][x]]
                    pygame.Surface.blit(
                        self.surface, IMAGES[tetromino.color], BOARD_TILE_RECTS[y][x])
