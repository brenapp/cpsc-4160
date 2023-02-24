import random
import pygame
import sys
import entity

ENTITIES = []
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN_COLOR = (255, 255, 255)

RECT_COLOR = (86, 50, 148)

pygame.init()
pygame.display.set_caption("pybox")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def sign(x): return -1 if x < 0 else (1 if x > 0 else 0)


class Player(entity.Entity):

    def __init__(self, id, init_state):

        init_state["laser_fire_rate"] = 250
        init_state["laser_cool_down"] = 0
        init_state["laser_count"] = 0

        init_state["rect"] = pygame.Rect(
            init_state["x_pos"], init_state["y_pos"], init_state["width"], init_state["height"])
        super().__init__(id, init_state)

    def update_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.state["accel_x"] = max(self.state["accel_x"] - 1, -10)
        if keys[pygame.K_RIGHT]:
            self.state["accel_x"] = min(self.state["accel_x"] + 1, 10)

        self.state["rect"].move_ip(self.state["accel_x"], 0)

        self.state["accel_x"] -= sign(self.state["accel_x"])

        if keys[pygame.K_UP] and self.state["laser_cool_down"] == 0:
            self.state["laser_cool_down"] = self.state["laser_fire_rate"]
            Laser("laser" + str(self.state["laser_count"] + 1), {
                "x_pos": self.state["rect"].x + self.state["rect"].width / 2,
                  "y_pos": self.state["rect"].y - 20,
                  "width": 5,
                  "height": 10,
                  "color": (255, 0, 0),
                  "accel_x": self.state["accel_x"]
                  })
            self.state["laser_count"] += 1

        if self.state["laser_cool_down"] > 0:
            self.state["laser_cool_down"] -= 1

    def handle_event(self, events):
        None

    def render(self):
        pygame.draw.rect(surface, self.state["color"], self.state["rect"])


class Laser(entity.Entity):

    def __init__(self, id, init_state):
        init_state["rect"] = pygame.Rect(
            init_state["x_pos"], init_state["y_pos"], init_state["width"], init_state["height"])
        init_state["accel_y"] = -1
        super().__init__(id, init_state)

    def update_state(self):

        self.state["rect"].move_ip(0, self.state["accel_y"])

        if self.state["rect"].y < 0:
            self.state["accel_y"] = 1
        elif self.state["rect"].y > SCREEN_HEIGHT:
            self.state["accel_y"] = -1

    def handle_event(self, events):
        None

    def render(self):
        pygame.draw.rect(surface, self.state["color"], self.state["rect"])


class Enemy(entity.Entity):

    def __init__(self, id, init_state):
        init_state["rect"] = pygame.Rect(
            init_state["x_pos"], init_state["y_pos"], init_state["width"], init_state["height"])
        super().__init__(id, init_state)
        player = entity.get_entity_by_id("player0")

    def update_state(self):
        difference = player.state["rect"].x - \
            self.state["rect"].x

        if abs(difference) < 60:
            self.state["rect"].move_ip(0, 1)
        elif difference > 0:
            self.state["rect"].move_ip(1, 0)
        elif difference < 0:
            self.state["rect"].move_ip(-1, 0)

    def handle_event(self, events):
        None

    def render(self):
        pygame.draw.rect(surface, self.state["color"], self.state["rect"])


player = Player("player0", {"x_pos": SCREEN_WIDTH / 2, "y_pos": SCREEN_HEIGHT - 100, "width": 80,
                            "height": 30, "color": RECT_COLOR, "accel_x": 0})

enemy_count = 0


def spawn_enemy():
    global enemy_count
    Enemy("enemy" + str(enemy_count), {"x_pos": random.randint(0, SCREEN_WIDTH), "y_pos": 100, "width": 80, "accel_x": 0,
                                       "height": 30, "color": (0, 0, 255), "player": player})
    enemy_count += 1


spawn_enemy()
spawn_enemy()


score = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.time.get_ticks() % 500 == 0:
        spawn_enemy()

    lasers = entity.get_all_entities_by_type("Laser")
    enemies = entity.get_all_entities_by_type("Enemy")

    for enemy in enemies:
        for laser in lasers:
            if laser.state["rect"].colliderect(enemy.state["rect"]):
                laser.remove()
                enemy.remove()
                score += 1

        if enemy.state["rect"].colliderect(player.state["rect"]):
            print("GAME OVER. Score: " + str(score))
            pygame.quit()
            sys.exit()

    for laser in lasers:
        if laser.state["rect"].colliderect(player.state["rect"]):
            laser.remove()
            player.remove()
            print("GAME OVER. Score: " + str(score))
            pygame.quit()
            sys.exit()

    surface.fill(SCREEN_COLOR)
    entity.stepAll()
    pygame.display.flip()
