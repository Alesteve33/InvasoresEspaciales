import pygame
import random
import math
from bullet import Bullet
from stats import Stats
from explosions import Explosions

class Boss:
    def __init__(self, x, y, boss_type, speed, direction, difficulty, player):
        self.x = x
        self.y = y
        self.boss_type = boss_type
        self.speed = speed

        self.player = player

        self.size = width, height = 404, 177

        self.isVisible = True

        self.sprite_number = 0
        self.animation_timer = 0
        self.animation_step = .1

        self.boss_image = pygame.transform.scale(pygame.image.load("sprites/boss/boss" + str(self.boss_type) + "_" + str(self.sprite_number) + ".png"), self.size)

        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0

        self.isOnSpawnAnimation = True
        self.spawnAnimationSpeed = 130
        self.distanceToPlayerToEndSpawnAnimation = 449

        self.explosionMaker = Explosions()
        self.isExploding = False
        self.finishedExplosion = False
        self.explosionStep = 0.1
        self.explosionTimer = 0
        self.explosionCount = 0
        self.hideAfterExplosionCount = 95
        self.explosionsToDo = 100
        self.waitAfterFinalExplosion = 3

        self.leftLaserEnabled = False
        self.rightLaserEnabled = False

        self.leftLaserTimer = 0
        self.rightLaserTimer = 0
        self.maxLaserTime = 3
        self.leftTimeSinceDisabled = 0
        self.rightTimeSinceDisabled = 0
        self.laserCooldown = 1

        self.randomShootChance = 10 #0.1
        self.randomLaserChance = 1 #0.001

        self.laser_image = pygame.transform.scale(pygame.image.load("sprites/laser.png"), (46, 415))
        self.left_laser_rect = self.laser_image.get_rect()
        self.right_laser_rect = self.laser_image.get_rect()

        self.direction = direction
        self.canShoot = True
        self.boss_rect = self.boss_image.get_rect()

        #Warning Rectangles
        self.warning_max_time = 2
        self.warnings = []
        self.right_warning_enabled = False
        self.left_warning_enabled = False

        self.maxHealth = -694201337
        if difficulty == 0: #Easy
            self.maxHealth = 15
            self.randomShootChance = 5
            self.warning_max_time = 3.5
            self.maxLaserTime = 2
        elif difficulty == 1: #Normal
            self.maxHealth = 20
            self.randomShootChance = 10
            self.warning_max_time = 2.5
            self.maxLaserTime = 3
        elif difficulty == 2: #Hard
            self.maxHealth = 30
            self.randomShootChance = 20
            self.warning_max_time = 1.5
            self.maxLaserTime = 4
        elif difficulty == 3: #Expert
            self.maxHealth = 40
            self.randomShootChance = 30
            self.warning_max_time = 1
            self.maxLaserTime = 5

        self.health = self.maxHealth

        self.rightWing = Wing(self.health / 3, "right", self.x, self.y, self)
        self.leftWing = Wing(self.health / 3, "left", self.x, self.y, self)

        pygame.Rect(self.boss_rect)

        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0

    def doAi(self, bullets, player, dt):
        if player.x - player.size[0] - 10 > self.left_laser_rect.x and player.x + player.size[0] + 10 < self.right_laser_rect.x and self.rightTimeSinceDisabled > self.laserCooldown and not self.left_warning_enabled and not self.right_warning_enabled and not self.rightLaserEnabled and not self.leftLaserEnabled:
            self.enableLaser(True, dt)
            self.enableLaser(False, dt)

        #if random.randint(0, 1000) > 1000 - self.randomLaserChance and self.timeSinceDisable > self.laserCooldown:
        #    self.enableLaser(True, dt)

        for i in range(4):
            if random.randint(0, 100) > 100 - self.randomShootChance:
                b = self.shootBoss1(i)
                if b is not None:
                    for bs in b:
                        bullets.append(bs)

    def drawBossBar(self, screen):
        x = screen.get_size()[0] / 5
        width = screen.get_size()[0] - 2 * x
        y = 20
        height = 30

        width2 = width - ((1 - (self.health / self.maxHealth)) * width)

        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x, y, width, height),  4)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x + 5, y + 5, width2 - 10, height - 10))


        x = screen.get_size()[0] / 8
        y = 70
        width = screen.get_size()[0] / 5
        height = 15

        width2 = width - ((1 - (self.leftWing.health / self.leftWing.maxHealth)) * width)

        if width2 > 0:
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x, y, width, height),  4)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x+2, y+2, width2 - 4, height-4))

        x = screen.get_size()[0] - screen.get_size()[0] / 8 - width

        width2 = width - ((1 - (self.rightWing.health / self.rightWing.maxHealth)) * width)

        if width2 > 0:
            pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x, y, width, height),  4)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x+2, y+2, width2-4, height-4))

    def enableLaser(self, isRightLaser, dt):
        if isRightLaser:
            warning = Warning(2)
            self.right_warning_enabled = True
            warning.followPos(self.right_laser_rect)
        else:
            warning = Warning(1)
            self.left_warning_enabled = True
            warning.followPos(self.left_laser_rect)

        warning.warning_image = pygame.transform.scale(warning.warning_image, self.laser_image.get_size())
        warning.warning_rect = warning.warning_image.get_rect()
        self.warnings.append(warning)


    def tick(self, dt, player, bullets):
        self.boss_rect.x = self.x
        self.boss_rect.y = self.y

        self.left_laser_rect.x = self.x + 79
        self.left_laser_rect.y = self.y + 120

        self.right_laser_rect.x = self.x + 279
        self.right_laser_rect.y = self.y + 120

        self.rightWing.x = self.x + 374
        self.leftWing.x = self.x - 63

        self.rightWing.y = self.y + 100
        self.leftWing.y = self.y + 100


        self.rightWing.tick(dt)
        self.leftWing.tick(dt)

        if self.health <= 0 and not self.isExploding:
            self.isExploding = True
            self.player.addScore(25)
            self.warnings = None

        if self.isExploding:
            self.explosionTimer += dt
            if self.explosionTimer >= self.explosionStep:
                if self.explosionsToDo >= self.explosionCount:
                    self.explosionTimer = 0
                    self.explosionCount += 1
                    self.explosionMaker.makeExplosion(self.x + random.randint(-60, 370),
                        self.y + random.randint(0, 30),
                        random.randint(100, 400))

            self.explosionMaker.tick(dt)


            if self.explosionCount >= self.hideAfterExplosionCount:
                self.isVisible = False

            if self.explosionsToDo <= self.explosionCount and self.explosionTimer > self.waitAfterFinalExplosion:
                self.finishedExplosion = True
            return

        if self.isOnSpawnAnimation:
            self.y += self.spawnAnimationSpeed * dt

            if self.y + self.distanceToPlayerToEndSpawnAnimation > player.y:
                self.isOnSpawnAnimation = False

            return

        self.animation_timer += dt
        self.animate()

        self.time_since_last_shot += dt

        if self.leftLaserEnabled:
            self.leftLaserTimer += dt
        if self.rightLaserEnabled:
            self.rightLaserTimer += dt
        if not self.rightLaserEnabled:
            self.rightTimeSinceDisabled += dt
        if not self.leftLaserEnabled:
            self.leftTimeSinceDisabled += dt

        if self.leftLaserTimer > self.maxLaserTime:
            self.leftLaserEnabled = False
            self.leftLaserTimer = round(random.uniform(0, self.maxLaserTime), 2)
            self.leftTimeSinceDisabled = 0
        if self.rightLaserTimer > self.maxLaserTime:
            self.rightLaserEnabled = False
            self.rightLaserTimer = round(random.uniform(0, self.maxLaserTime), 2)
            self.rightTimeSinceDisabled = 0



        for bullet in bullets:
            if bullet.isEnemyBullet is not True:
                if bullet.bullet_rect.colliderect(self.boss_rect) and self.leftWing.finishedExplosion and self.rightWing.finishedExplosion:
                    self.health -= bullet.damage
                    bullets.remove(bullet)
                if bullet.bullet_rect.colliderect(self.leftWing.wing_rect):
                    self.leftWing.health -= bullet.damage
                    if not self.left_warning_enabled and not self.leftLaserEnabled:
                        self.enableLaser(False, dt)
                    bullets.remove(bullet)
                if bullet.bullet_rect.colliderect(self.rightWing.wing_rect):
                    self.rightWing.health -= bullet.damage
                    bullets.remove(bullet)
                    if not self.right_warning_enabled and not self.rightLaserEnabled:
                        self.enableLaser(True, dt)

        #Warnings
        for warning in self.warnings:
            warning.animate(dt)
            if warning.type == 1:
                warning.followPos(self.left_laser_rect)
            elif warning.type == 2:
                warning.followPos(self.right_laser_rect)

            if warning.timer > self.warning_max_time:
                self.warnings.remove(warning)
                if warning.type == 1:
                    self.left_warning_enabled = False
                    self.leftLaserEnabled = True
                if warning.type == 2:
                    self.right_warning_enabled = False
                    self.rightLaserEnabled = True

        if player.health <= 0 or self.isExploding:
            self.warnings.clear()
        #if self.boss_type == 0:
        #    b = self.shootBoss1(3)
        #    if b is not None:
        #        for bs in b:
        #            bullets.append(bs)


        if self.leftLaserEnabled:
            if player.player_rect.colliderect(self.left_laser_rect):
                player.health = 0
        if self.rightLaserEnabled:
            if player.player_rect.colliderect(self.right_laser_rect):
                player.health = 0

        if self.direction == 0:
            self.x += self.speed * dt
        else:
            self.x -= self.speed * dt

        if self.x > 768 - self.size[0]:
            self.direction = 1
        elif self.x < 0:
            self.direction = 0

        self.explosionMaker.tick(dt)

    def shootBoss1(self, number):
        if self.time_since_last_shot > self.shoot_cooldown:
            self.time_since_last_shot = 0
            x = self.boss_rect.x
            y = self.boss_rect.centery

            if number == 0:
                x += 26
            elif number == 1:
                x += 152
            elif number == 2:
                x += 221
            else:
                x += 345

            return [Bullet(x, y, 400, True), Bullet(x + 9, y, 400, True), Bullet(x + 18, y, 400, True)]

    def animate(self):
        if self.animation_timer > self.animation_step:
            self.animation_timer = 0
            if self.sprite_number == 9:
                self.sprite_number = 1
            else:
                self.sprite_number += 1
            self.boss_image = pygame.transform.scale(pygame.image.load("sprites/boss/boss" + str(self.boss_type) + "_" + str(self.sprite_number) + ".png"), self.size)

    def render(self, screen):
        if not self.isOnSpawnAnimation and not self.isExploding:
            self.drawBossBar(screen)

        if self.isVisible:
            if self.leftLaserEnabled:
                screen.blit(self.laser_image, self.left_laser_rect)
            if self.rightLaserEnabled:
                screen.blit(self.laser_image, self.right_laser_rect)

            if self.warnings is not None:
                for warning in self.warnings:
                    warning.render(screen)

            screen.blit(self.boss_image, self.boss_rect)

            self.rightWing.render(screen)
            self.leftWing.render(screen)

        self.explosionMaker.render(screen)


class Wing:
    def __init__(self, health, orientation, x, y, boss):
        self.maxHealth = health
        self.health = self.maxHealth

        self.isExploding = False
        self.finishedExplosion = False
        self.wing_image = pygame.image.load("sprites/boss/" + orientation + ".png")
        self.wing_image = pygame.transform.scale(self.wing_image, tuple(x/5 for x in self.wing_image.get_size()))

        self.x = x
        self.y = y

        self.wing_rect = self.wing_image.get_rect()
        self.wing_rect.x = x
        self.wing_rect.y = y
        self.explosion = None
        self.boss = boss

    def tick(self, dt):
        self.wing_rect.x = self.x
        self.wing_rect.y = self.y

        if self.health <= 0 and not self.isExploding:
            self.isExploding = True
            self.boss.player.addScore(8)


    def render(self, screen):
        if self.isExploding and not self.finishedExplosion:
            self.explosion = self.boss.explosionMaker.makeExplosion(self.x - 140, self.y - 140, 400)
            print(self.explosion)
            self.finishedExplosion = True
        if self.health > 0:
            screen.blit(self.wing_image, self.wing_rect)
        elif self.isExploding:
            if self.explosion.currentAnimationFrame < 7:
                screen.blit(self.wing_image, self.wing_rect)


class Warning:
    def __init__(self, type):
        self.timer = 0
        self.timeForPeriod = 0.5
        self.actualAlpha = 0
        self.type = type  # 1 left, 2 right, 3 custom
        self.warning_image = pygame.image.load("sprites/fade.png")
        self.warning_rect = self.warning_image.get_rect()

        self.exclamation_image = pygame.image.load("sprites/exclamation.png")
        self.exclamation_image = pygame.transform.scale(self.exclamation_image, (100, 100))
        self.exclamation_rect = self.exclamation_image.get_rect()
        self.exclamation_rect.center = self.warning_rect.center


    def followPos(self, rect):
        self.warning_rect.topleft = rect.topleft
        self.exclamation_rect.center = self.warning_rect.center

    def render(self, screen):
        screen.blit(self.warning_image, self.warning_rect)
        screen.blit(self.exclamation_image, self.exclamation_rect)

    def animate(self, dt):
        self.timer += dt
        self.actualAlpha = 100 * math.sin(self.timer*8) + 155
        self.warning_image.set_alpha(self.actualAlpha)
        self.exclamation_image.set_alpha(self.actualAlpha)
        self.exclamation_image.fill((200, 0, 0), special_flags=pygame.BLEND_ADD)
