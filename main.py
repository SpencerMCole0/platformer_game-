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

def show_final_screen():
    show_text_screen("You Beat All Levels!", "Press R to Play Again or Q to Quit")
    return wait_for_key([pygame.K_r, pygame.K_q])

def load_level(level_num):
    enemy_speed = 1.5 + level_num * 0.8
    goal_y = HEIGHT - (80 + 40 * level_num)

    platform_list = [
        Platform(0, HEIGHT - 40, WIDTH, 40),
        Platform(300, 400 - 20 * level_num, 200, 20)
    ]
    is_flying = level_num >= 2
    goal = Goal(700, goal_y)
    enemy = Enemy(350, platform_list[1].y - 40, speed=enemy_speed, flying=is_flying)
    checkpoint = Checkpoint(500, HEIGHT - 70)

    return platform_list, goal, enemy, checkpoint

def run_level(level_num, spawn_override=None):
    spawn_point = spawn_override or [100, 100]
    player = Player(*spawn_point)
    checkpoint_reached = spawn_override is not None

    platforms, goal, enemy, checkpoint = load_level(level_num)

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
        enemy.update(player.x, player.y, platforms)

        if player.get_rect().colliderect(checkpoint.get_rect()):
            spawn_point = [checkpoint.x, checkpoint.y - player.height]
            checkpoint_reached = True

        if player.get_rect().colliderect(goal.get_rect()):
            return "next", None

        if player.get_rect().colliderect(enemy.get_rect()):
            key = show_game_over_screen(checkpoint_reached)
            if key == pygame.K_r:
                return "retry", None
            elif key == pygame.K_c and checkpoint_reached:
                return "checkpoint", spawn_point
            elif key == pygame.K_q:
                pygame.quit()
                sys.exit()

        player.draw(screen)
        for plat in platforms:
            plat.draw(screen)
        goal.draw(screen)
        enemy.draw(screen)
        checkpoint.draw(screen)

        pygame.display.flip()

    return "quit", None

# 🎮 Game loop
MAX_LEVEL = 3

while True:
    show_start_screen()

    level_num = 1
    checkpoint_state = None

    while level_num <= MAX_LEVEL:
        result, checkpoint_state = run_level(level_num, spawn_override=checkpoint_state)

        if result == "next":
            level_num += 1
            checkpoint_state = None
        elif result == "retry":
            checkpoint_state = None  # stay on same level
        elif result == "checkpoint":
            pass  # respawn on same level from checkpoint
        elif result == "quit":
            pygame.quit()
            sys.exit()

    final_key = show_final_screen()
    if final_key == pygame.K_r:
        continue
    else:
        pygame.quit()
        sys.exit()
