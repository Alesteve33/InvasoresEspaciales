import pygame

class Boss:
    def __init__(self, x, y, boss_type, speed, health, direction):
        self.x = x
        self.y = y
        self.boss_type = boss_type
        self.speed = speed
        self.size = width, height = 544, 256
        self.health = health

        self.isVisible = True

        self.sprite_number = 0
        self.animation_timer = 0
        self.animation_step = .1

        self.boss_image = pygame.transform.scale(pygame.image.load("sprites/boss" + str(self.boss_type) + "_" + str(self.sprite_number) + ".png"), self.size)

        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0

        self.laserEnabled = True
        self.laser_image = pygame.transform.scale(pygame.image.load("sprites/laser.png"), (46, 415))
        self.laser_rect = self.laser_image.get_rect()
        self.laser_rect_2 = self.laser_image.get_rect()

        self.direction = direction
        self.canShoot = True
        self.boss_rect = self.boss_image.get_rect()

    def tick(self, dt):
        self.animation_timer += dt
        self.animate()

        self.boss_rect.x = self.x
        self.boss_rect.y = self.y

        self.laser_rect.x = self.x + 149
        self.laser_rect.y = 260

        self.laser_rect_2.x = self.x + 349
        self.laser_rect_2.y = 260


        if self.direction == 0:
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt

        if self.x > 768 - self.size[0]:
            self.direction = 1
        elif self.x < 0:
            self.direction = 0

    def animate(self):
        if self.animation_timer > self.animation_step:
            self.animation_timer = 0
            if self.sprite_number == 9:
                self.sprite_number = 1
            else:
                self.sprite_number += 1
            self.boss_image = pygame.transform.scale(pygame.image.load("sprites/boss" + str(self.boss_type) + "_" + str(self.sprite_number) + ".png"), self.size)

    def render(self, screen):
        if not self.isVisible:
            return

        if self.laserEnabled:
            screen.blit(self.laser_image, self.laser_rect)
            screen.blit(self.laser_image, self.laser_rect_2)
        screen.blit(self.boss_image, self.boss_rect)
