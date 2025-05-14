import pygame
import sys
import random
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

def show_game_over_screen():
    show_text_screen("Game Over", "Press R to Restart or Q to Quit")
    return wait_for_key([pygame.K_r, pygame.K_q])

def load_level(level_num):
    random.seed(level_num)

    enemy_speed = min(1.5 + level_num * 0.4, 4.0)
    num_steps = 3 + level_num

    platform_list = []
    ground = Platform(0, HEIGHT - 40, WIDTH, 40)
    platform_list.append(ground)

    x, y = 100, HEIGHT - 100
    for _ in range(num_steps):
        width = random.randint(120, 220)
        platform_list.append(Platform(x, y, width, 20))
        x = max(0, min(x + random.randint(-100, 100), WIDTH - width))
        y = max(60, y - random.randint(50, 90))

    goal_platform = platform_list[-1]
    goal_x = goal_platform.x + goal_platform.width - 40
    goal_y = goal_platform.y - 40
    goal = Goal(goal_x, goal_y)

    mid_x = (50 + goal_x) // 2
    platforms_above_ground = platform_list[1:-1]
    checkpoint_platform = min(platforms_above_ground, key=lambda p: abs((p.x + p.width // 2) - mid_x))
    checkpoint_x = checkpoint_platform.x + (checkpoint_platform.width // 2) - 15
    checkpoint_y = checkpoint_platform.y - 30
    checkpoint = Checkpoint(checkpoint_x, checkpoint_y)
    checkpoint_rect = pygame.Rect(checkpoint_x, checkpoint_y, 30, 30)

    enemies = []
    platforms_used = set()

    enemy_platform_candidates = [
        plat for plat in platform_list[1:-1]
        if plat != checkpoint_platform
    ]

    max_enemies = min(level_num + 1, len(enemy_platform_candidates))
    for _ in range(max_enemies):
        plat = random.choice(enemy_platform_candidates)
        if plat in platforms_used and plat.width < 160:
            continue

        ex = plat.x + random.randint(0, max(10, plat.width - 40))
        ey = plat.y - 40
        e_rect = pygame.Rect(ex, ey, 40, 40)

        if e_rect.colliderect(checkpoint_rect):
            continue

        flying = random.choice([True, False])
        enemies.append(Enemy(ex, ey, speed=enemy_speed, flying=flying))
        platforms_used.add(plat)

    return platform_list, goal, enemies, checkpoint

def run_level(level_num, player, spawn_override=None):
    spawn_point = spawn_override or [50, HEIGHT - 100]
    checkpoint_reached = spawn_override is not None
    player.x, player.y = spawn_point
    player.vel_y = 0
    player.invincible_timer = 0

    platforms, goal, enemies, checkpoint = load_level(level_num)

    running = True
    paused = False

    while running:
        clock.tick(60)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        if not paused:
            player.handle_input()
            player.apply_gravity()
            player.check_collision(platforms)
            player.update_invincibility()

            for enemy in enemies:
                enemy.update(player.x, player.y, platforms)
                if player.get_rect().colliderect(enemy.get_rect()):
                    player.take_damage()
                    if player.hp <= 0:
                        player.lives -= 1
                        if player.lives < 0:
                            return "game_over", None
                        else:
                            return "retry", None

            if player.get_rect().colliderect(checkpoint.get_rect()):
                spawn_point = [checkpoint.x, checkpoint.y - player.height]
                checkpoint_reached = True

            if player.get_rect().colliderect(goal.get_rect()):
                if player.hp < player.max_hp:
                    player.hp += 1
                return "next", None

        player.draw(screen)
        player.draw_health(screen, font_small)
        for plat in platforms:
            plat.draw(screen)
        goal.draw(screen)
        checkpoint.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        level_label = font_small.render(f"Level: {level_num}", True, (0, 0, 0))
        screen.blit(level_label, (10, 40))

        if paused:
            pause_msg = font_small.render("Paused – Press P to Resume", True, (0, 0, 0))
            screen.blit(pause_msg, (WIDTH // 2 - pause_msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

# 🎮 Main Game Loop
while True:
    show_start_screen()
    level_num = 1
    checkpoint_state = None
    player = Player(50, HEIGHT - 100)

    while True:
        result, checkpoint_state = run_level(level_num, player, spawn_override=checkpoint_state)

        if result == "next":
            level_num += 1
            checkpoint_state = None
        elif result == "retry":
            player.hp = player.max_hp
            checkpoint_state = None
        elif result == "game_over":
            key = show_game_over_screen()
            if key == pygame.K_r:
                break  # restart full game
            else:
                pygame.quit()
                sys.exit()
        elif result == "quit":
            pygame.quit()
            sys.exit()
        