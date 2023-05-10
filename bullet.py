import pygame

class Bullet:
    def __init__(self, x, y, speed, isEnemyBullet):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = width, height = 16, 16

        self.isEnemyBullet = isEnemyBullet

        self.damage = 1

        self.bullet_image = pygame.transform.scale(pygame.image.load("sprites/bullet.png"), self.size)
        self.bullet_rect = self.bullet_image.get_rect()

    def render(self, screen):
        screen.blit(self.bullet_image, self.bullet_rect)

    def tick(self, deltaTime):
        if self.isEnemyBullet:
            self.y += self.speed * deltaTime
        else:
            self.y -= self.speed * deltaTime

        self.bullet_rect.x = self.x
        self.bullet_rect.y = self.y
