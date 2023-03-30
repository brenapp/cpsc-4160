# Milestone #1 - Progress Update

<img width="1552" alt="image" src="https://user-images.githubusercontent.com/8839926/228336492-7c3700c3-7d68-44b7-8fae-c23d12524298.png">

> Developers: Brendan McGuire, Darin Spitzer, Chase Dunlap
> 30 March 2023

# Game Concept

We began this milestone figuring out the details of our game concept. The basic concept of the game
expanded from two basic ideas we wanted to explore: some sort of tetris based game and exploring
platformer mechanics such as jumping and moving. We decided to combine these two ideas into a single
2 player asymmetric tetris platformer game.

In the game, one player controls the environment (the board) by placing Tetrominoes into the field
of play. The other player controls a frog that must navigate the board to avoid the falling pieces.
The frog's goal is to reach the top of the board, while the board player's goal is to prevent this
from happening by clearing lines.

The Tetris-esque parts of the game are meant to feel slightly like Tetris but with a vastly
different game plan required to succeed. The platformer player has a completely unique goal of
climbing to the top of the screen and avoiding falling tiles.

In addition to these base mechanics, we plan on adding a number of additional power ups each player
can collect and utilize:

- Custom pieces (pieces that are not standard tetrominoes)
- Tetromino piece speed
- Custom moves for the frog (double jump, wall jump, etc.)

# Goals

For this milestone, we set the following goals (completed goals are marked with a checkmark):

- [x] Basic Tetris Implementation

  - [x] Piece Rendering
  - [x] Basic Controls
  - [x] Spawn New pieces
  - [x] Piece Movement & Rotation

- [x] Tetris Stretch Goals:

  - [x] Next Piece Preview
  - [x] Hold Piece

- [ ] Agent Navigation

  - [x] Agent Sprites
  - [ ] Basic Keyboard Navigation (Move and Jump)
  - [ ] Collision with non-active tetrominos

- [ ] Agent Stretch Goals
  - [ ] Sprite Animation (multiple sprites)
  - [ ] Game over when active piece hits frog

# Features Discussion

<img width="1552" alt="image" src="https://user-images.githubusercontent.com/8839926/228336656-12d21002-9ecb-4726-92e9-58443c1d72d0.png">

This sprint, we really wanted to focus on getting the core mechanics of the game implemented, which
we were able to do successfully.

# Technical Details

This section outlines some of the implementation details we used to achieve the features listed
above.

## Entity Component System

Initially, we utilized a [Model View
Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) system to organize
our code, but we quickly realized that this was not the best system for our game. We decided to
switch to a simplified [Entity Component System](https://en.wikipedia.org/wiki/Entity_component_system) (ECS)
to organize our code. In an Entity Component System, individual elements of the game (board,
individual pieces, etc.) are represented as entities, with each entity having a number of state
variables (position, color, etc.).

This structure allows us to easily maintain code separation between different parts of the game

## Tetris Board

The tetris board is implemented using 2 structures: (1) a list of in-play Tetrominos, and (2) a
2D array of tiles, which stores the index of the tetromino that occupies that tile, or `None` if
empty. This allows us to easily check for collisions and render the board.

```python
class Board(entity.Entity):

    cells = [[None for x in range(BOARD_WIDTH)]
             for y in range(BOARD_HEIGHT)]

    tetrominos: list[entities.tetromino.Tetromino] = []
    active_tetromino = None
```

> [`entities/board.py`](../entities/board.py)

To render the board, each individual tile is rendered as its own `Rect`, whose color is determined
by the active piece on that tile (if any). This allows us to easily update the model of tile
placement without having to manually move sprites in pygame, which would be difficult to maintain.

```python
BOARD_TILE_RECTS = [[pygame.Rect(BOARD_X + x * CELL_WIDTH, BOARD_Y + y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                     for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]


 for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board.cells[y][x] is not None:
                    tetromino = self.board.tetrominos[self.board.cells[y][x]]
                    pygame.Surface.blit(
                        self.surface, IMAGES[tetromino.color], BOARD_TILE_RECTS[y][x])
```

> [`systems/render_board.py`](../systems/render_board.py)

## Defining Pieces

When designing the Tetromino system, we wanted to account for custom piece shapes, so we designed a generic system that can be used to move and rotate any generic piece. Each tetromino type has a `base_tile` and a number of `offset_tiles`

```python
class Tetromino(entity.Entity):

    def __init__(self, index, base_tile, tiles, color):
        self.index = index
        self.base_tile = base_tile
        self.tiles = tiles
        self.color = color

    def get_absolute_tiles(self):
        return [(self.base_tile[0] + tile[0], self.base_tile[1] + tile[1]) for tile in self.tiles]

# ...
```

> [`entities/tetromino.py`](../entities/tetromino.py)

Each type of tetromino is defined as a number of block offsets from the base tile. This allows us to quickly add new and custom pieces in the future that are not the typical pieces found in a standard game. _Importantly, the center of rotation is defined at the base tile, so you must be careful to define your offsets in such a way as to ensure they rotate correctly_

```python

I_PIECE = [(-1, 0), (0, 0), (1, 0), (2, 0)]
J_PIECE = [(-1, -1), (-1, 0), (0, 0), (1, 0)]
L_PIECE = [(-1, 0), (0, 0), (1, 0), (1, -1)]
O_PIECE = [(0, 0), (1, 0), (0, 1), (1, 1)]
S_PIECE = [(-1, 0), (0, 0), (0, 1), (1, 1)]
Z_PIECE = [(-1, 1), (-1, 0), (0, 0), (1, 0)]
T_PIECE = [(-1, 0), (0, 0), (1, 0), (0, 1)]
```

### Rotation

As mentioned above, the center of rotation is defined as the base tile. This allows us to easily implement piece rotation by applying a 90deg [rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix#Common_rotations).

```
rotation = [[0, -1] # 90 deg
            [1, 0]]

rotate(x, y) = rotation * (x, y)
= (x, y)[[0, -1] = (0x + 1y, -1x + 0y) = (y, -x)
         [1, 0]]
```

Because each tile is implemented as an offset from `(0, 0)`, implementing this rotation vector allows us to easily rotate each piece about its base tile. Not all pieces in tetris rotate about the center of their base tile, but

![image](https://user-images.githubusercontent.com/8839926/228342514-9bb99c80-d84a-498c-95d6-1ac314d05623.png)

> The centers of rotation for each piece. Not all of them are purely in the center of the base tile, but this system provides a quick approximation for this behavior without needing to define individual offsets for each rotation.

# Goals for Next Milestone

We want to accomplish the following goals for the next milestone:

- [ ] Implement proper endgame detection for the frog agent
- [ ] Improve game theming (theme tetris aspect, add additional animations)
- [ ] Iterate on player controls
- [ ] Add proper play and game over screens
- [ ] Add Powerups:
  - [ ] Add
