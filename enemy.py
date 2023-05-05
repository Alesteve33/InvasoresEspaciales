import pygame
import random
from bullet import Bullet

class Enemy:
    def __init__(self, x, y, enemy_type, speed, health, direction):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.speed = speed
        self.size = width, height = 48, 48
        self.health = health
        self.enemy_image = pygame.transform.scale(pygame.image.load("sprites/enemy_0.png"), self.size)
        
        self.shoot_cooldown = 0.4
        self.time_since_last_shot = 0
        
        self.direction = direction
        
        self.setType(0)
        self.enemy_rect = self.enemy_image.get_rect()
        
    
    def tick(self, bullets, px, py, deltaTime, bulletRand):
        
        self.enemy_rect.x = self.x
        self.enemy_rect.y = self.y
        
        self.time_since_last_shot += deltaTime

        #if self.x + 10 > px and self.x - 10 < px:
        if self.x == px:
            b = self.shoot()
            if b is not None:
                bullets.append(b)
        elif random.randint(0, 100) > bulletRand:
            b = self.shoot()
            if b is not None:
                bullets.append(b)

        for bullet in bullets:
            if bullet.isEnemyBullet is not True:
                if bullet.bullet_rect.colliderect(self.enemy_rect):
                    self.health -= bullet.damage
                    bullets.remove(bullet)
                
        
    def setType(self, e_type):
        if e_type == 0:
            self.enemy_image = pygame.transform.scale(pygame.image.load("sprites/enemy_0.png"), self.size)
            self.enemy_image = pygame.transform.rotate(self.enemy_image, 180)
            
    def render(self, screen):
        screen.blit(self.enemy_image, self.enemy_rect)

    def shoot(self):
        if self.time_since_last_shot > self.shoot_cooldown and random.randint(1, 100) >= 95:
            self.time_since_last_shot = 0
            return Bullet(self.enemy_rect.centerx - 8, self.enemy_rect.centery - 20, 400, True)


