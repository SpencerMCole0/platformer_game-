# player.py
import pygame

GRAVITY = 0.8
JUMP_STRENGTH = -15

class Player:
    def __init__(self, x, y):
        self.width = 50
        self.height = 50
        self.color = (50, 150, 255)
        self.x = x
        self.y = y
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def check_collision(self, platforms):
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
