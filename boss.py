import pygame
import random
from bullet import Bullet

from explosions import Explosions

class Boss:
    def __init__(self, x, y, boss_type, speed, health, direction):
        self.x = x
        self.y = y
        self.boss_type = boss_type
        self.speed = speed

        self.size = width, height = 404, 177

        self.maxHealth = health
        self.health = self.maxHealth

        self.MaxWingHealth = health / 3
        self.LeftWingHealth = self.MaxWingHealth
        self.RightWingHealth = self.MaxWingHealth

        self.isVisible = True

        self.sprite_number = 0
        self.animation_timer = 0
        self.animation_step = .1

        self.boss_image = pygame.transform.scale(pygame.image.load("sprites/boss/boss" + str(self.boss_type) + "_" + str(self.sprite_number) + ".png"), self.size)
        self.left_wing_image = pygame.image.load("sprites/boss/left.png")
        self.left_wing_image = pygame.transform.scale(self.left_wing_image, tuple(x/5 for x in self.left_wing_image.get_size()))
        self.right_wing_image = pygame.image.load("sprites/boss/right.png")
        self.right_wing_image = pygame.transform.scale(self.right_wing_image, tuple(x/5 for x in self.right_wing_image.get_size()))

        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0

        self.isOnSpawnAnimation = True
        self.spawnAnimationSpeed = 130
        self.distanceToPlayerToEndSpawnAnimation = 500

        self.explosionMaker = Explosions()
        self.isExploding = False
        self.finishedExplosion = False
        self.explosionStep = 0.1
        self.explosionTimer = 0
        self.explosionCount = 0
        self.hideAfterExplosionCount = 95
        self.explosionsToDo = 100
        self.waitAfterFinalExplosion = 3

        self.laserEnabled = True

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
        self.right_wing_rect = self.right_wing_image.get_rect()
        self.left_wing_rect = self.left_wing_image.get_rect()

        
        
        
        pygame.Rect(self.boss_rect)
        
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

        width = 80 
        height = 15

        width2 = width - ((1 - (self.LeftWingHealth / self.MaxWingHealth)))
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x, y, width, height),  4)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x+2, y+2, width2 - 4, height-4))

        width2 = width - ((1 - (self.LeftWingHealth / self.MaxWingHealth)))

        x = screen.get_size()[0] - screen.get_size()[0] / 8 - width
        y = 70

        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x, y, width-4, height-4),  4)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x+2, y+2, width2-4, height-4))

    def tick(self, dt, player, bullets):
        self.boss_rect.x = self.x
        self.boss_rect.y = self.y
        self.right_wing_rect.bottomright = (self.boss_rect.bottomright[0] +65, self.boss_rect.bottomright[1] + 43) 
        self.left_wing_rect.bottomleft = (self.boss_rect.bottomleft[0] -66, self.boss_rect.bottomleft[1] + 43) 

        self.laser_rect.x = self.x + 79
        self.laser_rect.y = self.y + 120

        self.laser_rect_2.x = self.x + 279
        self.laser_rect_2.y = self.y + 120

        if self.health <= 0:
            self.isExploding = True

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
                if bullet.bullet_rect.colliderect(self.boss_rect) or bullet.bullet_rect.colliderect(self.left_wing_rect) or bullet.bullet_rect.colliderect(self.right_wing_rect):
                    self.health -= bullet.damage
                    bullets.remove(bullet)

        #if self.boss_type == 0:
        #    b = self.shootBoss1(3)
        #    if b is not None:
        #        for bs in b:
        #            bullets.append(bs)


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
            if self.laserEnabled:
                screen.blit(self.laser_image, self.laser_rect)
                screen.blit(self.laser_image, self.laser_rect_2)
            screen.blit(self.boss_image, self.boss_rect)
            screen.blit(self.right_wing_image, self.right_wing_rect)
            screen.blit(self.left_wing_image, self.left_wing_rect)
            

        self.explosionMaker.render(screen)
