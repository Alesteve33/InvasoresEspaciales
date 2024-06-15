import pygame
import math

class Shield:
    def __init__(self):
        self.actualAlpha = 100
        self.size = 200, 200

        self.shield_image = pygame.transform.scale(pygame.image.load("sprites/shield_1.png"), self.size)
        self.sprite_number = 1

        self.shield_rect = self.shield_image.get_rect()

        self.animation_timer = 0
        self.animation_step = .2
        self.animationSpeed = 1
        self.shieldMaxTime = 6
        self.opacityTimer = 0

        self.cooldown_timer = 1000
        self.cooldown = 5

        self.isEnabled = False

        self.indicator = Indicator(self.cooldown)

        self.enableShieldSound = pygame.mixer.Sound("sounds/shield_enabled.mp3")
        self.disableShieldSound = pygame.mixer.Sound("sounds/shield_disabled.mp3")

    def enableShield(self):
        if self.cooldown_timer > self.cooldown and not self.isEnabled:
            self.enableShieldSound.play()
            self.isEnabled = True
            self.cooldown_timer = 0
            self.animation_timer = 0
            self.opacityTimer = 0
            self.animation_step = 0.2
            self.animationSpeed = 1
            self.shield_image.set_alpha(255)

    def tick(self, dt, px, py, ps):
        self.shield_rect.x = px + ps/2 - self.size[0]/2
        self.shield_rect.y = py - 45

        self.animation_timer += dt
        if not self.isEnabled:
            self.cooldown_timer += dt
        if self.animation_timer > self.shieldMaxTime and self.isEnabled:
            self.disableShield()

        self.indicator.tick(dt)


    def render(self, screen):
        if self.isEnabled:
            screen.blit(self.shield_image, self.shield_rect)
            self.indicator.render(screen)
            
    def disableShield(self):
        self.disableShieldSound.play()
        self.isEnabled = False

    def animate(self, dt):
        if self.animation_timer > self.animation_step:
            self.animation_step += 0.2
            if self.sprite_number == 6:
                self.sprite_number = 1
            else:
                self.sprite_number += 1
            self.shield_image = pygame.transform.scale(pygame.image.load("sprites/shield_" + str(self.sprite_number) + ".png"), self.size)
        if self.animation_timer > self.shieldMaxTime / 3:
            self.opacityTimer += dt
            self.animationSpeed += dt
            self.actualAlpha = 100 * math.cos(self.opacityTimer*self.animationSpeed) + 155
            self.shield_image.set_alpha(self.actualAlpha)


class Indicator:
    def __init__(self, cooldown):
        self.angle = 0
        self.timer = 0
        self.cooldown = cooldown
        self.x = 100
        self.y = 100
        self.radius = 20
    
    def tick(self, dt):
        self.angle += dt
        
    def render(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), ((self.x, self.y),
                                                      (math.cos(self.angle), math.sin(self.angle)),
                                                      (math.cos(self.angle) * self.x, math.sin(self.angle))))
