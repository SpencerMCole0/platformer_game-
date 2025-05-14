# goal.py
import pygame

class Goal:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
