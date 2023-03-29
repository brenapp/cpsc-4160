from . import entity


class ClampedValue:

    def __init__(self, value, min_value, max_value):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def set(self, value):
        self.value = max(self.min_value, min(self.max_value, value))

    def add(self, value):
        self.set(self.value + value)

    def clamp(self, min, max):
        self.min_value = min
        self.max_value = max

    def is_clamped(self):
        return self.value == self.min_value or self.value == self.max_value

    def __repr__(self):
        return f"ClampedValue({self.value}, {self.min_value}, {self.max_value})"


class Frog(entity.Entity):

    pos: tuple[ClampedValue, 2]
    vel: tuple[ClampedValue, 2]
    acc: tuple[ClampedValue, 2]

    def __init__(self, board, pos_x, pos_y):

        self.pos = (
            ClampedValue(pos_x, 0, 0),
            ClampedValue(pos_y, 0, 0)
        )

        self.vel = (
            ClampedValue(0, 0, 0),
            ClampedValue(0, 0, 0)
        )

        self.acc = (
            ClampedValue(0, 0, 0),
            ClampedValue(0, 0, 0)
        )

    def apply_force(self, x, y):
        self.acc[0].add(x)
        self.acc[1].add(y)

    def step_kinematics(self):

        self.vel[0].add(self.acc[0].value)
        self.vel[1].add(self.acc[1].value)
        self.pos[0].add(self.vel[0].value)
        self.pos[1].add(self.vel[1].value)

        self.acc[0].set(0)
        self.acc[1].set(0)
