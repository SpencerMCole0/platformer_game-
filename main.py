import pygame
import sys
from player import Player
from platform import Platform # type: ignore
from goal import Goal
from enemy import Enemy
from checkpoint import Checkpoint

# Initialize game
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Spawn & checkpoint setup
spawn_point = [100, 100]
player = Player(*spawn_point)

# Game objects
platforms = [
    Platform(0, HEIGHT - 40, WIDTH, 40),     # Ground
    Platform(300, 400, 200, 20),             # Floating platform
]

goal = Goal(700, HEIGHT - 80)
enemy = Enemy(350, 360)  # On top of floating platform
checkpoint = Checkpoint(500, HEIGHT - 70)

# Win screen
def show_win_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("You Win!", True, (0, 200, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill((135, 206, 235))  # Sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input and physics
    player.handle_input()
    player.apply_gravity()
    player.check_collision(platforms)

    # Enemy movement
    enemy.update()

    # Checkpoint reached
    if player.get_rect().colliderect(checkpoint.get_rect()):
        spawn_point = [checkpoint.x, checkpoint.y - player.height]

    # Goal reached
    if player.get_rect().colliderect(goal.get_rect()):
        show_win_screen()

    # Enemy collision = respawn
    if player.get_rect().colliderect(enemy.get_rect()):
        player.x, player.y = spawn_point
        player.vel_y = 0

    # Draw everything
    player.draw(screen)
    for plat in platforms:
        plat.draw(screen)
    goal.draw(screen)
    enemy.draw(screen)
    checkpoint.draw(screen)

    pygame.display.flip()

# Quit game
pygame.quit()
sys.exit()
