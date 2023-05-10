import pygame

class Fade:
    def __init__(self):
        self.fade = pygame.image.load_extended('sprites/fade.png').convert_alpha()
        self.alpha = 255
        self.fadeState = 0
        self.fadeSpeed = 2

    def render(self, screen):
        self.fade.set_alpha(self.alpha)
        screen.blit(self.fade, (0, 0))

    def tick(self):
        if self.fadeState == 1: #FADE IN
            self.alpha -= self.fadeSpeed
        elif self.fadeState == 2: #FADE OUT
            self.alpha += self.fadeSpeed

        if self.alpha > 255:
            self.alpha = 255
        elif self.alpha < 0:
            self.alpha = 0

    def setFadeState(self, fadeState):
        self.fadeState = fadeState
