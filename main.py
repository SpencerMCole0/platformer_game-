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
    random.seed(level_num)

    enemy_speed = 1.5 + level_num * 0.8
    num_steps = 3 + level_num

    platform_list = []
    ground = Platform(0, HEIGHT - 40, WIDTH, 40)
    platform_list.append(ground)

    # Step-up platform pattern
    x, y = 100, HEIGHT - 100
    for _ in range(num_steps):
        width = random.randint(120, 220)
        platform_list.append(Platform(x, y, width, 20))
        x = max(0, min(x + random.randint(-100, 100), WIDTH - width))
        y = max(60, y - random.randint(50, 90))

    # Goal on top platform
    goal_platform = platform_list[-1]
    goal_x = goal_platform.x + goal_platform.width - 40
    goal_y = goal_platform.y - 40
    goal = Goal(goal_x, goal_y)

    # Midpoint between start (x=50) and goal
    mid_x = (50 + goal_x) // 2
    platforms_above_ground = platform_list[1:]
    checkpoint_platform = min(platforms_above_ground, key=lambda p: abs((p.x + p.width // 2) - mid_x))
    checkpoint_x = checkpoint_platform.x + (checkpoint_platform.width // 2) - 15
    checkpoint_y = checkpoint_platform.y - 30
    checkpoint = Checkpoint(checkpoint_x, checkpoint_y)

    # Enemies
    enemies = []

    # 1 enemy guarding checkpoint
    guard_x = checkpoint_platform.x + random.randint(0, max(10, checkpoint_platform.width - 40))
    guard_y = checkpoint_platform.y - 40
    guard_flying = random.choice([True, False])
    enemies.append(Enemy(guard_x, guard_y, speed=enemy_speed, flying=guard_flying))

    # Add more enemies
    for _ in range(level_num):
        plat = random.choice(platforms_above_ground)
        ex = plat.x + random.randint(0, max(10, plat.width - 40))
        ey = plat.y - 40
        flying = random.choice([True, False])
        enemies.append(Enemy(ex, ey, speed=enemy_speed, flying=flying))

    return platform_list, goal, enemies, checkpoint

def run_level(level_num, spawn_override=None):
    # Safe ground spawn or checkpoint
    if spawn_override:
        spawn_point = spawn_override
        checkpoint_reached = True
    else:
        spawn_point = [50, HEIGHT - 100]
        checkpoint_reached = False

    player = Player(*spawn_point)
    platforms, goal, enemies, checkpoint = load_level(level_num)

    running = True
    paused = False

    while running:
        clock.tick(60)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            player.handle_input()
            player.apply_gravity()
            player.check_collision(platforms)

            for enemy in enemies:
                enemy.update(player.x, player.y, platforms)
                if player.get_rect().colliderect(enemy.get_rect()):
                    key = show_game_over_screen(checkpoint_reached)
                    if key == pygame.K_r:
                        return "retry", None
                    elif key == pygame.K_c and checkpoint_reached:
                        return "checkpoint", spawn_point
                    elif key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            if player.get_rect().colliderect(checkpoint.get_rect()):
                spawn_point = [checkpoint.x, checkpoint.y - player.height]
                checkpoint_reached = True

            if player.get_rect().colliderect(goal.get_rect()):
                return "next", None

        # Draw everything
        player.draw(screen)
        for plat in platforms:
            plat.draw(screen)
        goal.draw(screen)
        checkpoint.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        if paused:
            pause_msg = font_small.render("Paused – Press P to Resume", True, (0, 0, 0))
            screen.blit(pause_msg, (WIDTH // 2 - pause_msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

# Game loop
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
            checkpoint_state = None
        elif result == "checkpoint":
            pass
        elif result == "quit":
            pygame.quit()
            sys.exit()

    final_key = show_final_screen()
    if final_key == pygame.K_r:
        continue
    else:
        pygame.quit()
        sys.exit()
