import pygame

class Explosions():
    def __init__(self):
        self.explosions = []

    def tick(self, dt):
        for explosion in self.explosions:
            explosion.tick(dt)

    def render(self, screen):
        for explosion in self.explosions:
            explosion.render(screen)

    def makeExplosion(self, x, y, size):
        self.explosions.append(Explosion(x, y, size))

class Explosion():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.animationTimer = 0
        self.animationFrameTime = 0.15
        self.waitTimeAfterFinishedExplosion = 2
        self.currentAnimationFrame = 1
        self.explosion_image = pygame.transform.scale(pygame.image.load("sprites/Circle_explosion1.png"), (self.size, self.size))
        self.explosion_rect = self.explosion_image.get_rect()

        self.explosion_rect.x = self.x
        self.explosion_rect.y = self.y


    def render(self, screen):
        if self.currentAnimationFrame < 10 or self.animationTimer < self.animationFrameTime:
            screen.blit(self.explosion_image, self.explosion_rect)

    def tick(self, dt):
        self.animationTimer += dt
        if self.animationTimer > self.animationFrameTime and self.currentAnimationFrame < 10:
            self.animationTimer = 0

            self.currentAnimationFrame += 1
            self.explosion_image = pygame.transform.scale(pygame.image.load("sprites/Circle_explosion" + str(self.currentAnimationFrame) + ".png"), (self.size, self.size))
            self.explosion_rect = self.explosion_image.get_rect()

            self.explosion_rect.x = self.x
            self.explosion_rect.y = self.y
