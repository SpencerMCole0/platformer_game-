# checkpoint.py
import pygame

class Checkpoint:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 215, 0)  # gold

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
