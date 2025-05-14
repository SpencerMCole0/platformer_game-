# enemy.py
import pygame
import math

GRAVITY = 0.5

class Enemy:
    def __init__(self, x, y, width=40, height=40, speed=2, range_to_follow=300, flying=False):
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

    def update(self, player_x, player_y, platforms):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.range_to_follow:
            if self.flying:
                self.apply_gravity()
                self.check_platform_collision(platforms)

                # Try horizontal tracking first
                if abs(dx) > 5:
                    if dx < 0:
                        self.x -= self.speed * 0.6
                    else:
                        self.x += self.speed * 0.6

                # Only move vertically if not blocked by platform above
                if abs(dy) > 5:
                    vertical_rect = self.get_rect().move(0, self.speed * 0.6 if dy > 0 else -self.speed * 0.6)
                    if not any(vertical_rect.colliderect(p.get_rect()) for p in platforms):
                        self.y += self.speed * 0.6 if dy > 0 else -self.speed * 0.6
            else:
                if dx < 0:
                    self.x -= self.speed
                elif dx > 0:
                    self.x += self.speed

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def check_platform_collision(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.get_rect().colliderect(plat.get_rect()):
                if self.vel_y > 0:
                    self.y = plat.y - self.height
                    self.vel_y = 0
                    self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
