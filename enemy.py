# enemy.py
import pygame

class Enemy:
    def __init__(self, x, y, width=40, height=40, speed=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (255, 0, 0)

    def update(self, player_x):
        if player_x < self.x:
            self.x -= self.speed
        elif player_x > self.x + self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
