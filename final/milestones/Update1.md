# Milestone #1 - Progress Update

<img width="1552" alt="image" src="https://user-images.githubusercontent.com/8839926/228336492-7c3700c3-7d68-44b7-8fae-c23d12524298.png">


> Developers: Brendan McGuire, Darin Spitzer, Chase Dunlap
> 30 March 2023

# Game Concept

We began this milestone figuring out the details of our game concept. The basic concept of the game 

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


# Technical Changes

## Tetris Board
Each 

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

Each type of tetromino is defined as a number of block offsets from the base tile. This allows us to quickly add new and custom pieces in the future that are not the typical pieces found in a standard game. *Importantly, the center of rotation is defined at the base tile, so you must be careful to define your offsets in such a way as to ensure they rotate correctly*

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
> The centers of rotation for each piece. Not all of them are purely in the center of the base tile, but this system provides a quick approximation for this behavior without needing to define invidual offsets for each rotation. 


## Entity Component System
