# main.py
import pygame
import sys
from player import Player
from platform import Platform

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

player = Player(100, 100)
platforms = [
    Platform(0, HEIGHT - 40, WIDTH, 40),  # Ground
    Platform(300, 400, 200, 20),          # Floating platform
]

running = True
while running:
    clock.tick(60)
    screen.fill((135, 206, 235))  # Sky blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input()
    player.apply_gravity()
    player.check_collision(platforms)
    player.draw(screen)

    for plat in platforms:
        plat.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
