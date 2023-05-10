import pygame

class Shield:
    def __init__(self):

        self.size = 200, 200

        self.shield_image = pygame.transform.scale(pygame.image.load("sprites/shield_1.png"), self.size)
        self.sprite_number = 1

        self.shield_rect = self.shield_image.get_rect()

        self.animation_timer = 0
        self.animation_step = .2

        self.cooldown_timer = 10
        self.cooldown = 5

        self.isEnabled = False

        self.enableShieldSound = pygame.mixer.Sound("sounds/shield_enabled.mp3")
        self.disableShieldSound = pygame.mixer.Sound("sounds/shield_disabled.mp3")

    def enableShield(self):
        if self.cooldown_timer > self.cooldown and not self.isEnabled:
            self.enableShieldSound.play()
            self.isEnabled = True
            self.cooldown_timer = 0

    def tick(self, dt, px, py, ps):
        self.shield_rect.x = px + ps/2 - self.size[0]/2
        self.shield_rect.y = py - 45

        self.animation_timer += dt
        self.cooldown_timer += dt

    def render(self, screen):
        if self.isEnabled:
            screen.blit(self.shield_image, self.shield_rect)

    def animate(self):
        if self.animation_timer > self.animation_step:
            self.animation_timer = 0
            if self.sprite_number == 6:
                self.sprite_number = 1
            else:
                self.sprite_number += 1
            self.shield_image = pygame.transform.scale(pygame.image.load("sprites/shield_" + str(self.sprite_number) + ".png"), self.size)
