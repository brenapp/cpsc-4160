import random

I_PIECE = [(-1, 0), (0, 0), (1, 0), (2, 0)]
J_PIECE = [(-1, -1), (-1, 0), (0, 0), (1, 0)]
L_PIECE = [(0, -1), (0, 0), (0, 1), (1, 1)]
O_PIECE = [(0, 0), (1, 0), (0, 1), (1, 1)]
S_PIECE = [(0, 0), (1, 0), (-1, 1), (0, 1)]
Z_PIECE = [(0, 0), (-1, 0), (0, 1), (1, 1)]
T_PIECE = [(0, 0), (-1, 1), (0, 1), (1, 1)]

PIECES = [I_PIECE, J_PIECE, L_PIECE,  O_PIECE, S_PIECE, Z_PIECE, T_PIECE]
COLORS = [(130, 255, 130), (0, 255, 0), (239, 132, 72),
          (209, 171, 44), (165, 201, 64), (210, 92, 151), (255, 0, 0), (242, 110, 98)]


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
        return (PIECES[tile], COLORS[tile])
