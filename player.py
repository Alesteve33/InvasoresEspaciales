import pygame
from bullet import Bullet
from shield import Shield

class Player:
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = width, height = 64, 73
        self.health = health
        
        self.shield = Shield()
        
        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 1
        
        self.player_image = pygame.transform.scale(pygame.image.load("sprites/player_1.png"), self.size)
        self.player_rect = self.player_image.get_rect()
        
    def render(self, screen):
        screen.blit(self.player_image, self.player_rect)
        self.shield.render(screen)
    
    def tick(self, deltaTime, bullets):
        self.shield.tick(deltaTime, self.x, self.y, self.size[0])
        self.shield.animate()
        
        self.time_since_last_shot += deltaTime
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        
        bulletsToDestroy = []
        for bullet in bullets:
            if bullet.isEnemyBullet:
                if bullet.bullet_rect.colliderect(self.player_rect):
                    bulletsToDestroy.append(bullet)
                    if self.shield.isEnabled:
                        self.shield.isEnabled = False
                    else:    
                        self.health -= bullet.damage
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
            
            
        