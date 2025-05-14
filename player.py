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

        # ❤️ Health and lives
        self.max_hp = 5
        self.hp = self.max_hp
        self.lives = 3
        self.invincible_timer = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        self.x = max(0, min(self.x, 800 - self.width))
        self.y = max(0, min(self.y, 600 - self.height))

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def check_collision(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.get_rect().colliderect(plat.get_rect()):
                if self.vel_y > 0 and self.get_rect().bottom - self.vel_y <= plat.y + 5:
                    self.y = plat.y - self.height
                    self.vel_y = 0
                    self.on_ground = True

    def take_damage(self, amount=1):
        if self.invincible_timer == 0:
            self.hp -= amount
            if self.hp <= 0:
                self.lives -= 1
                self.hp = self.max_hp
            self.invincible_timer = 60  # 1 second of invincibility

    def update_invincibility(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

    def draw_health(self, screen, font):
        # Draw hearts or HP blocks
        for i in range(self.hp):
            pygame.draw.rect(screen, (255, 0, 0), (10 + i * 22, 10, 20, 20))
        for i in range(self.lives):
            pygame.draw.circle(screen, (0, 0, 0), (750 - i * 25, 20), 10)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
