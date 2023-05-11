import pygame
import random
from bullet import Bullet

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

        self.laserEnabled = False

        self.laserTimer = 0
        self.maxLaserTime = 3
        self.timeSinceDisable = 0
        self.laserCooldown = 3

        self.randomShootChance = 10 #0.1
        self.randomLaserChance = 1 #0.001

        self.laser_image = pygame.transform.scale(pygame.image.load("sprites/laser.png"), (46, 415))
        self.laser_rect = self.laser_image.get_rect()
        self.laser_rect_2 = self.laser_image.get_rect()

        self.direction = direction
        self.canShoot = True
        self.boss_rect = self.boss_image.get_rect()

        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0

    def doAi(self, bullets, player):
        if player.x - player.size[0] - 10 > self.laser_rect.x and player.x + player.size[0] + 10 < self.laser_rect_2.x and self.timeSinceDisable > self.laserCooldown:
            self.laserEnabled = True

        if random.randint(0, 1000) > 1000 - self.randomLaserChance and self.timeSinceDisable > self.laserCooldown:
            self.laserEnabled = True

        for i in range(4):
            if random.randint(0, 100) > 100 - self.randomShootChance:
                b = self.shootBoss1(i)
                if b is not None:
                    for bs in b:
                        bullets.append(bs)

    def tick(self, dt, player, bullets):
        self.animation_timer += dt
        self.animate()

        self.time_since_last_shot += dt

        if self.laserEnabled:
            self.laserTimer += dt
        else:
            self.timeSinceDisable += dt

        if self.laserTimer > self.maxLaserTime:
            self.laserEnabled = False
            self.laserTimer = round(random.uniform(0, self.maxLaserTime), 2)
            self.timeSinceDisable = 0

        self.doAi(bullets, player)

        for bullet in bullets:
            if bullet.isEnemyBullet is not True:
                if bullet.bullet_rect.colliderect(self.boss_rect):
                    self.health -= bullet.damage
                    print(self.health)
                    bullets.remove(bullet)

        #if self.boss_type == 0:
        #    b = self.shootBoss1(3)
        #    if b is not None:
        #        for bs in b:
        #            bullets.append(bs)

        self.boss_rect.x = self.x
        self.boss_rect.y = self.y

        self.laser_rect.x = self.x + 149
        self.laser_rect.y = 260

        self.laser_rect_2.x = self.x + 349
        self.laser_rect_2.y = 260


        if self.laserEnabled:
            if player.player_rect.colliderect(self.laser_rect) or player.player_rect.colliderect(self.laser_rect_2):
                player.health = 0

        if self.direction == 0:
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt

        if self.x > 768 - self.size[0]:
            self.direction = 1
        elif self.x < 0:
            self.direction = 0

    def shootBoss1(self, number):
        if self.time_since_last_shot > self.shoot_cooldown:
            self.time_since_last_shot = 0
            x = self.boss_rect.x
            y = self.boss_rect.centery

            if number == 0:
                x += 96
            elif number == 1:
                x += 216
            elif number == 2:
                x += 296
            else:
                x += 416

            return [Bullet(x, y, 400, True), Bullet(x + 9, y, 400, True), Bullet(x + 18, y, 400, True)]

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
