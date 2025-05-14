import pygame

class Enemy:
    def __init__(self, x, y, width=40, height=40, speed=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 0, 0)
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left
        self.range = 100    # total movement range
        self.start_x = x

    def update(self):
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) >= self.range:
            self.direction *= -1  # switch direction

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
