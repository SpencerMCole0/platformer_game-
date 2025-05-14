import pygame
import sys
from player import Player
from platform import Platform
from goal import Goal
from enemy import Enemy

# Initialize game
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Game objects
player = Player(100, 100)

platforms = [
    Platform(0, HEIGHT - 40, WIDTH, 40),     # Ground
    Platform(300, 400, 200, 20),             # Floating platform
]

goal = Goal(700, HEIGHT - 80)
enemy = Enemy(350, 360)  # On top of floating platform

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

# Game over screen
def show_game_over_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game Over", True, (200, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill((135, 206, 235))  # Sky blue background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    player.handle_input()
    player.apply_gravity()
    player.check_collision(platforms)

    enemy.update()

    # Collision checks
    if player.get_rect().colliderect(goal.get_rect()):
        show_win_screen()

    if player.get_rect().colliderect(enemy.get_rect()):
        show_game_over_screen()

    # Drawing
    player.draw(screen)
    for plat in platforms:
        plat.draw(screen)
    goal.draw(screen)
    enemy.draw(screen)

    pygame.display.flip()

# Quit game
pygame.quit()
sys.exit()
