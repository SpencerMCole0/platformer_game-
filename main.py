import pygame
import sys
from player import Player
from platform import Platform
from goal import Goal
from enemy import Enemy
from checkpoint import Checkpoint

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def show_text_screen(title, subtitle):
    screen.fill((255, 255, 255))
    title_surf = font_big.render(title, True, (0, 0, 0))
    subtitle_surf = font_small.render(subtitle, True, (100, 100, 100))
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def wait_for_key(valid_keys):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in valid_keys:
                return event.key

def show_start_screen():
    show_text_screen("Platformer Game", "Press SPACE to Start")
    wait_for_key([pygame.K_SPACE])

def show_win_screen():
    show_text_screen("You Win!", "Press R to Restart or Q to Quit")
    return wait_for_key([pygame.K_r, pygame.K_q])

def show_game_over_screen(checkpoint_reached):
    if checkpoint_reached:
        show_text_screen("Game Over", "R = Restart | C = Continue | Q = Quit")
        return wait_for_key([pygame.K_r, pygame.K_c, pygame.K_q])
    else:
        show_text_screen("Game Over", "R = Restart | Q = Quit")
        return wait_for_key([pygame.K_r, pygame.K_q])

def run_game(spawn_override=None):
    # Player setup
    spawn_point = spawn_override or [100, 100]
    player = Player(*spawn_point)
    checkpoint_reached = spawn_override is not None

    platforms = [
        Platform(0, HEIGHT - 40, WIDTH, 40),
        Platform(300, 400, 200, 20),
    ]

    goal = Goal(700, HEIGHT - 80)
    enemy = Enemy(350, 360)
    checkpoint = Checkpoint(500, HEIGHT - 70)

    running = True
    while running:
        clock.tick(60)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_input()
        player.apply_gravity()
        player.check_collision(platforms)
        enemy.update()

        if player.get_rect().colliderect(checkpoint.get_rect()):
            spawn_point = [checkpoint.x, checkpoint.y - player.height]
            checkpoint_reached = True

        if player.get_rect().colliderect(goal.get_rect()):
            key = show_win_screen()
            return key, None

        if player.get_rect().colliderect(enemy.get_rect()):
            key = show_game_over_screen(checkpoint_reached)
            if key == pygame.K_r:
                return key, None
            elif key == pygame.K_c and checkpoint_reached:
                return key, spawn_point
            elif key == pygame.K_q:
                pygame.quit()
                sys.exit()

        # Draw everything
        player.draw(screen)
        for plat in platforms:
            plat.draw(screen)
        goal.draw(screen)
        enemy.draw(screen)
        checkpoint.draw(screen)

        pygame.display.flip()

    return pygame.K_q, None

# Main loop
while True:
    show_start_screen()
    checkpoint_state = None

    while True:
        result, checkpoint_state = run_game(spawn_override=checkpoint_state)
        if result == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif result == pygame.K_r:
            checkpoint_state = None  # full restart
        elif result == pygame.K_c:
            pass  # keep checkpoint_state
