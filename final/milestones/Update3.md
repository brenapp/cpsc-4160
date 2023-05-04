# Milestone #2 - Final Submission

<img width="1012" alt="Screenshot 2023-05-03 at 9 59 24 PM" src="https://user-images.githubusercontent.com/8839926/236097952-c4c1dfaf-7975-4b80-bd59-dee5d3558261.png">

## Milestone Goals

We did not accomplish all of the stretch goals we set out for this milestone, we added a number of
features and overall polish with the game that we are very satisfied with. Over the course of the
semester, we produced a fun, engaging playable game that is a faithful implementation of one concept,
and would be a great starting point for a more complete game.

- [ ] Implement the cling state

  - [ ] Game Logic and Mechanics
  - [ ] Art & Animations

- [ ] Add a scoring system

  - [ ] Based on original tetris scoring system for the player, and a frog survival score for the frog

- [x] Add more game over states

  - [x] Squashed by a tetromino
  - [x] Frog trapped and can't escape

- [x] Add some sort of power ups that give each player additional abilities

  - [ ] Frog Double Jump
  - [x] Tetris Slam Piece or Speed Boost

- [x] General Refactors
  - [x] Integrate frog state into the frog entity, for better code sharing between the render system
        and the frog input system

## Better Collisions & Game Over Detection

One of the biggest functionality issues we struggled with throughout this project was handling the
collisions between the frog and the tetrominos. In particular, we really struggled with the frog
glitching through walls and jumping up whenever it collided with a wall. In this update, we
introduced an approach to try and fix this behavior, the secondary collider.

The frog's secondary collider sits above the frog's main collider, and is used to detect collisions
horizontally when the frog has colliding with an object. By detecting collisions with the secondary
collider, we were able to better handle situations where the frog is simultaneously colliding with
multiple tiles at once, causing it to spasm out.

```python
  match(self.state):

            case FrogStateGrounded(collider):

                # Jumping handled in player_input()
                self.frog.collider.move_ip(0, 1)

                colliding = self.colliding_any(candidates)
                if colliding is None:
                    self.state = FrogStateAirborne()
                    self.frog.status = "airborne"
                else:

                    # Get all rects colliding
                    colliding = self.frog.collider.collidelistall(candidates)

                    for i in colliding:

                        # if the frog is completely within the collision candidate, game over
                        overlap_horizontal = max(
                            0, min(self.frog.collider.right, candidates[i].right) - max(self.frog.collider.left, candidates[i].left))

                        within_vertical = (self.frog.collider.top >= candidates[i].top) and (
                            self.frog.collider.bottom <= candidates[i].bottom)

                        if within_vertical and overlap_horizontal > 10:
                            self.game_status.winner = status.Winner.TETRIS

                self.frog.collider.move_ip(0, -1)

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

> [systems/frog_input.py](../systems/frog_input.py)

## Updated Theming & General Polish

<img width="1012" alt="Screenshot 2023-05-03 at 10 00 23 PM" src="https://user-images.githubusercontent.com/8839926/236097996-b948c2cd-fbe9-4b92-a1d6-e5a19b80908e.png">


We also utilized the time in this milestone to add some additional graphics and polish to the game.
One of the features introduced was a better concept of "game status", with a global entity which
represents the current game status (recorded as the winner and if the game has ended). This allowed
us to have a custom system to define behavior if the game has ended, and stop running systems on
game over.

```python
class GameStatus(entity.Entity):

    winner: Winner = Winner.NONE
    game_over = False
```

> [entities/game_status.py](../entities/game_status.py)

With the game status entity, we can define and update system behavior whenever the game ends, and
add a custom ending game screen which declares the winners and freezes until the user exits.

```python
class GameFlow(system.System):

    surface: pygame.Surface
    game_status: status.GameStatus
    font: pygame.font.Font

    def __init__(self, surface, status):
        self.surface = surface
        self.game_status = status
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

        super().__init__()

    def run(self, entities, events):

        if self.game_status.winner != status.Winner.NONE:
            if self.game_status.winner == status.Winner.FROG:
                self.surface.blit(pygame.image.load(
                    "assets/frog_win.png"), (0, 0))
            else:
                self.surface.blit(pygame.image.load(
                    "assets/tetris_win.png"), (0, 0))

            pygame.display.flip()
            self.game_status.game_over = True
```

> [systems/game_flow.py](../systems/game_flow.py)

## Frog Scream Ability

<img width="1012" alt="Screenshot 2023-05-03 at 9 59 24 PM" src="https://user-images.githubusercontent.com/8839926/236098007-1c771dff-e6ce-46e7-a8ca-f089a01c36e1.png">


One of the final features we introduced was the concept of a "frog scream". This is a special
ability the frog has to counteract the fact that it is relatively easy to trap the frog into
impossible situations. The frog scream is activated by pressing the E key, and allows the frog to
emit a loud scream that will destroy the first tetromino piece it comes into contact with. This
ability is currently limited to once every 4 seconds for balance.

Implementing this feature was _relatively_ straightforward, due to the Entity Component System we
adopted earlier in the project development. First, we created a `Shockwave` Entity type, which had a
number of properties on it:

```python
class Shockwave(entity.Entity):

    collider: pygame.Rect
    vel: tuple[ClampedValue, 2]

    def __init__(self, x, y):

        self.collider = pygame.Rect(x, y, SHOCKWAVE_SIZE, SHOCKWAVE_SIZE)
        self.vel = (
            ClampedValue(0, -10, 10),
            ClampedValue(0, -10, 10)
        )

        super().__init__()

    def step_kinematics(self):
        self.collider.x += self.vel[0].value
        self.collider.y += self.vel[1].value

```

> [entities/shockwave.py](../entities/shockwave.py)
