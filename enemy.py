import pygame
import math
import random

GRAVITY = 0.5

class Enemy:
    def __init__(self, x, y, width=30, height=30, speed=2, range_to_follow=300, flying=False):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.width = width
        self.height = height
        self.speed = speed
        self.range_to_follow = range_to_follow
        self.flying = flying
        self.color = (255, 0, 0)
        self.on_ground = False

        self.mode = "patrol"
        self.direction = random.choice([-1, 1])
        self.mood_timer = random.randint(180, 300)

    def update(self, player_x, player_y, platforms):
        self.mood_timer -= 1
        if self.mood_timer <= 0:
            self.mode = "chase" if self.mode == "patrol" else "patrol"
            self.mood_timer = random.randint(180, 300)
            if self.mode == "patrol":
                self.direction = random.choice([-1, 1])

        dx = player_x - self.x
        dy = player_y - self.y

        if self.mode == "chase" and math.hypot(dx, dy) < self.range_to_follow:
            if self.flying:
                self.apply_gravity()
                self.check_platform_collision(platforms)

                if abs(dx) > 10:
                    self.x += self.speed * 0.4 * (1 if dx > 0 else -1)
                if abs(dy) > 10:
                    vertical_move = self.speed * 0.4 * (1 if dy > 0 else -1)
                    test_rect = self.get_rect().move(0, vertical_move)
                    if not any(test_rect.colliderect(p.get_rect()) for p in platforms):
                        self.y += vertical_move
            else:
                if abs(dx) > 10:
                    self.x += self.speed * 0.6 * (1 if dx > 0 else -1)
        else:
            self.x += self.direction * self.speed * 0.3

            if self.flying:
                self.apply_gravity()
                self.check_platform_collision(platforms)

            if not self.flying:
                edge_buffer = 10
                future_x = self.x + self.direction * edge_buffer
                foot_rect = pygame.Rect(future_x, self.y + self.height + 1, self.width, 2)
                if not any(foot_rect.colliderect(p.get_rect()) for p in platforms):
                    self.direction *= -1

            if random.random() < 0.005:
                self.direction *= -1

        self.x = max(0, min(self.x, 800 - self.width))
        self.y = min(self.y, 600 - self.height)

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def check_platform_collision(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.get_rect().colliderect(plat.get_rect()):
                if self.vel_y > 0 and self.get_rect().bottom - self.vel_y <= plat.y + 10:
                    self.y = plat.y - self.height
                    self.vel_y = 0
                    self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
