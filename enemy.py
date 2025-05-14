# enemy.py
import pygame
import math

class Enemy:
    def __init__(self, x, y, width=40, height=40, speed=2, range_to_follow=300, flying=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.range_to_follow = range_to_follow
        self.flying = flying
        self.color = (255, 0, 0)

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.range_to_follow:
            if self.flying:
                # Normalize direction vector
                if distance != 0:
                    dx /= distance
                    dy /= distance
                    self.x += dx * self.speed
                    self.y += dy * self.speed
            else:
                if player_x < self.x:
                    self.x -= self.speed
                elif player_x > self.x + self.width:
                    self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
