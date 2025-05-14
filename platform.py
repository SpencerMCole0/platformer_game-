# platform.py
import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.color = (139, 69, 19)  # Brown
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
