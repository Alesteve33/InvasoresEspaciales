import pygame
from bullet import Bullet
from shield import Shield

class Player:
    def __init__(self, x, y, speed, health, menu, stats):
        self.x = x
        self.y = y

        self.speed = speed
        self.size = width, height = 64, 73
        self.health = health

        self.shield = Shield()
        
        self.menu = menu
        self.stats = stats
        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 1

        self.isExploding = False
        self.finishedExplosion = False
        
        self.animationTimer = 0
        self.animationFrameTime = 0.15
        self.waitTimeAfterFinishedExplosion = 2
        self.currentAnimationFrame = 1
        self.explosion_image = pygame.image.load("sprites/Circle_explosion1.png")
        self.explosion_rect = self.explosion_image.get_rect()

        self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_1.png"), self.size)
        self.player_rect = self.player_image.get_rect()
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        self.score = 0

        self.health_sound = pygame.mixer.Sound("sounds/health.mp3")
    def render(self, screen, dt):
        if self.currentAnimationFrame < 7:
            screen.blit(self.player_image, self.player_rect)
            self.shield.render(screen)

        if self.isExploding:
            self.animationTimer += dt
            if self.animationTimer > self.animationFrameTime and self.currentAnimationFrame < 10:
                self.animationTimer = 0
                self.animateExplosion()
            self.explosion_rect.centerx = self.player_rect.centerx
            self.explosion_rect.centery = self.player_rect.centery

            if self.currentAnimationFrame < 10 or self.animationTimer < self.animationFrameTime:
                screen.blit(self.explosion_image, self.explosion_rect)
        if self.currentAnimationFrame >= 10:
            self.animationTimer += dt
            if self.animationTimer > self.waitTimeAfterFinishedExplosion:
                self.finishedExplosion = True



    def tick(self, deltaTime, bullets):
        self.shield.tick(deltaTime, self.x, self.y, self.size[0])
        self.shield.animate(deltaTime)

        self.time_since_last_shot += deltaTime
        self.player_rect.x = self.x
        self.player_rect.y = self.y

        bulletsToDestroy = []
        for bullet in bullets:
            if bullet.isEnemyBullet:
                if bullet.bullet_rect.colliderect(self.player_rect):
                    bulletsToDestroy.append(bullet)
                    if self.shield.isEnabled:
                        pass
                    else:
                        self.health -= bullet.damage
                        self.health_sound.play()
        for bullet in bulletsToDestroy:
            bullets.remove(bullet)

        if self.health >= 4:
            self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_1.png"), self.size)
        elif self.health < 4 and self.health >= 3:
            self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_2.png"), self.size)
        elif self.health < 3 and self.health >= 2:
            self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_3.png"), self.size)
        elif self.health < 2 and self.health > 0:
            self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_4.png"), self.size)
        else:
            return False
        return True

    def animateExplosion(self):
        self.currentAnimationFrame += 1
        self.explosion_image = pygame.transform.scale(pygame.image.load("sprites/Circle_explosion" + str(self.currentAnimationFrame) + ".png"), (500,500))
        self.explosion_rect = self.explosion_image.get_rect()

    def handleKey(self, keys, deltaTime):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            self.x -= self.speed * deltaTime
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < 768 - self.size[0]:
            self.x += self.speed * deltaTime
        if keys[pygame.K_s]:
            self.shield.enableShield()

    def shoot(self):
        if self.time_since_last_shot > self.shoot_cooldown:
            self.time_since_last_shot = 0
            return Bullet(self.player_rect.centerx - 8, self.player_rect.centery - 20, 1000, False)

    def addScore(self, multiplier):
        scoreToAdd = 0
        if self.menu.difficulty == 0:
           scoreToAdd = 1 * multiplier
        elif self.menu.difficulty == 1:
           scoreToAdd = 2 * multiplier
        elif self.menu.difficulty == 2:
           scoreToAdd = 3 * multiplier
        elif self.menu.difficulty == 3:
           scoreToAdd = 5 * multiplier
        self.score += scoreToAdd
        self.stats.totalScore += scoreToAdd
