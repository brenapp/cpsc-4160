# Milestone #2 - Progress Update

> Developers: Brendan McGuire, Darin Spitzer, Chase Dunlap
> 18 April 2023

The focus of this update was to introduce the secondary player character, the Frog. The frog is
controller by a second player and must navigate the board to avoid the falling pieces. The frog's
objective is to get to the top of the screen, while the board player's goal is to prevent this from
happening, and squash the frog with a falling piece.

## Milestone Goals

We set the following goals for this milestone (completed goals are marked with a checkmark). While
we didn't achieve every goal that we set out to achieve, we made significant progress on the core
mechanics of the game.

Implementing effective collisions between the moving pieces and the frog proved to be very
challenging, and took significantly more development time than we had anticipated. However, we were
also able to make significant progress on the theming of the game, and we were able to add a number
of custom animations to the frog, and improve the background of the game.

- [x] Frog Navigation

  - [x] Fix collisions with Tetris blocks
  - [x] Handle game-over situations (collisions with active tetromino, reaching top of the board)
  - [x] Iterate on the control scheme
  - [x] Add more movements (wall jumps, double jumps)

- [ ] Power-Ups:

  - [ ] Add the ability for tetris and frog players to collect power-ups

- [ ] Themeing:
  - [x] Improve theming of Tetris element
  - [x] Add animations for idling, jumping, and walking
  - [ ] Introduction Screen and Game Over Screen

## Frog Control

We implemented the frog as a State Machine, with the following states:

- Grounded: The frog is standing on the ground or a tetromino
- Airborne: The frog is not contacting the ground or a tetromino
- Clinging: THe frog is touching a tetromino, but not standing on it (not yet implemented)

```python
@dataclass
class FrogStateGrounded:
    collider: pygame.Rect


@dataclass
class FrogStateAirborne:
    pass


FrogState = FrogStateGrounded | FrogStateAirborne
```

> [`systems/frog_input.py`](../systems/frog_input.py)

Then, we could implement a number of transitions between each frog state, allowing us to quickly and
cleanly define the behavior of the frog. For example, consider the _player-defined_ transitions,
which allow the user to control the frog's movement. We can see how the exact movement
characteristics are based on the state of the frog, and how the frog's state can be updated based on
user input.

```python
def player_input(self):

        keys = pygame.key.get_pressed()

        self.frog.vel[0].set(0)

        if keys[pygame.K_a]:
            if isinstance(self.state, FrogStateGrounded):
                self.frog.vel[0].set(-3)
                self.frog.direction = "left"
            else:
                self.frog.vel[0].set(-1)
                self.frog.direction = "left"

        elif keys[pygame.K_d]:
            if isinstance(self.state, FrogStateGrounded):
                self.frog.vel[0].set(3)
                self.frog.direction = "right"
            else:
                self.frog.vel[0].set(1)
                self.frog.direction = "right"

        if keys[pygame.K_w] and not isinstance(self.state, FrogStateAirborne):
            self.frog.vel[1].set(-3)
            self.state = FrogStateAirborne()
            self.frog.status = "airborne"
```

> [`systems/frog_input.py`](../systems/frog_input.py)

## Collisions

Collisions proved to be extremely tricky to implement. One of the challenges is that the _collision
candidates_–the objects that the frog could collide with–change every frame. This means the first
step is computing all of the rects that could be colliding with the frog each frame. Thankfully, we
designed the board such that each cell is its own `pygame.Rect`, so the process of finding
collisions candidates is simply a matter of iterating over the board and finding all of the cells
which are occupied by a tetromino.

```python
def get_collision_candidates(self):
        candidates = [BOARD_LEFT_WALL_RECT,
                      BOARD_RIGHT_WALL_RECT, BOARD_BOTTOM_RECT]
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.board.cells[y][x] is None:
                    continue

                candidates.append(BOARD_TILE_RECTS[y][x])

        return candidates
```

> [`systems/frog_input.py`](../systems/frog_input.py)

We include the board walls here to ensure that the frog can't leave the board. Once we have the
collision candidates, we need to check which candidates are actually colliding with the frog. The
exact way we check the collisions is based on the current state, as different collisions imply
different state transitions

```python
match(self.state):

  case FrogStateGrounded(collider):

      # Jumping handled in player_input()

      self.frog.collider.move_ip(0, 1)

      if self.colliding_any(candidates) is None:
          self.state = FrogStateAirborne()
          self.frog.status = "airborne"

      self.frog.collider.move_ip(0, -1)
```

> [`systems/frog_input.py`](../systems/frog_input.py)

If the frog is grounded to a collider, we check if the frog is colliding with any of the candidates
and if not, we transition to the airborne state. Note that our definition of _colliding_ in this
context means that the frog is 1 pixel above colliding with the candidate. This allows us to cleanly
seperate out vertical and horizontal collisions without any additional special logic, and the
`FrogStateGround` state keeps track of the colliding we are contacting.

```python
case FrogStateAirborne():

  self.frog.collider.move_ip((0, self.frog.vel[1].value))
  collision = self.colliding_any(candidates)

  altered = False

  while self.colliding_any(candidates) is not None:
      self.frog.collider.move_ip(
          0, -sign(self.frog.vel[1].value))
      altered = True

  if altered:
      self.state = FrogStateGrounded(collider=collision)
      self.frog.status = "idle"
```

> [`systems/frog_input.py`](../systems/frog_input.py)

If we are airborne, and we are colliding with a candidate, we change our state to grounded. However,
since we are working from the assumption that the frog is 1 pixel above colliding with the
candidate, when they transition to grounded, we must move the frog's collider up/down to ensure that
the frog is _no longer_ colliding with the candidate.

We handle vertical and horizontal collisions separately, as it makes the logic much simpler.
Conveniently, collisions in the horizontal direction currently do not require state specific logic,
so they can be handled simply.

```python
if (self.frog.vel[0].value != 0):
  self.frog.collider.move_ip((self.frog.vel[0].value, 0))

  altered = False

  while self.colliding_any(candidates) is not None:
      self.frog.collider.move_ip(
          -sign(self.frog.vel[0].value), 0)
      altered = True

  if altered:
      self.frog.vel[0].set(0)
```

Horizontal collision will be complicated by the introduction of the cling state in a future update,
but it should be relatively easy to apply a number of state transitions for similar logic. For
example, if the frog is airborne and collides horizontally with a tetromino, we could transition to
the clinging state.

## Animations

This update also introduced a number of custom animations and sprites for the frog based on it's
current state. The idle animation is a simple 5 frame animation that is triggered when the frog is
not moving.

```python
frameNum = pygame.time.get_ticks()
idletime = frameNum % 600
if(self.frog.status != "airborne"):
    self.airtime = 0
if (self.frog.status == "idle"):
    if (idletime >= 0 and idletime < 100):
        self.image = IMAGES["FROG"]
    if (idletime >= 100 and idletime < 200):
        self.image = IMAGES["FROG_IDLE1"]
    if (idletime >= 200 and idletime < 300):
        self.image = IMAGES["FROG_IDLE2"]
    if (idletime >= 300 and idletime < 400):
        self.image = IMAGES["FROG_IDLE3"]
    if (idletime >= 400 and idletime < 500):
        self.image = IMAGES["FROG_IDLE4"]
    if (idletime >= 500 and idletime < 600):
        self.image = IMAGES["FROG_IDLE5"]
```

> [`systems/render_frog.py`](../systems/render_frog.py)

We defined a similar animation for the frog's airborne state, with a simple 5 frame animation when
the frog first transitions to airborne

```python
if (self.frog.status == "airborne"):
    if (self.airtime >= 0 and self.airtime < 1):
        self.image = IMAGES["FROG"]
    if (self.airtime >= 1 and self.airtime < 3):
        self.image = IMAGES["FROG_JUMP1"]
    if (self.airtime >= 3 and self.airtime < 6):
        self.image = IMAGES["FROG_JUMP2"]
    if (self.airtime >= 6 and self.airtime < 9):
        self.image = IMAGES["FROG_JUMP3"]
    if (self.airtime >= 9 and self.airtime < 12):
        self.image = IMAGES["FROG_JUMP4"]
    if (self.airtime >= 12 and self.airtime < 15):
        self.image = IMAGES["FROG_JUMP5"]
    if (self.airtime >= 15):
        self.image = IMAGES["FROG_JUMP6"]
    self.airtime += 1
```

> [`systems/render_frog.py`](../systems/render_frog.py)

Finally, we flip all animations based on the direction the frog is facing.

```python
if (self.frog.direction == "left"):
    pygame.Surface.blit(self.surface, pygame.transform.flip(self.image, True, False),
                        (self.frog.collider.x, self.frog.collider.y))
elif (self.frog.direction == "right"):
    pygame.Surface.blit(
        self.surface, self.image, (self.frog.collider.x, self.frog.collider.y - 10))
```

> [`systems/render_frog.py`](../systems/render_frog.py)

# Goals for the Future

As the end of the semester is approaching quickly, we want to get our game to a reasonable
implementation state. We are focusing on the core game mechanics, and will be adding additional
features as time permits.

- [ ] Implement the cling state

  - [ ] Game Logic and Mechanics
  - [ ] Art & Animations

- [ ] Add a scoring system

  - [ ] Based on original tetris scoring system for the player, and a frog survival score for the frog

- [ ] Add more game over states

  - [ ] Squashed by a tetromino
  - [ ] Frog trapped and can't escape

- [ ] Add some sort of power ups that give each player additional abilities

  - [ ] Frog Double Jump
  - [ ] Tetris Slam Piece or Speed Boost

- [ ] General Refactors
  - [ ] Integrate frog state into the frog entity, for better code sharing between the render system
        and the frog input system
