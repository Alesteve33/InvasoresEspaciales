import pygame
import random

class Background:
    def __init__(self, sw, sh):
        self.size =  1000, 672
        self.animationSpeed = 2.0
        self.timer = 0
        self.planetSpawnCooldown = 0
        self.lastPlanetXPos = 0 
        self.backgroundElements = []
        
        starsCount = 2
        planetCount = 2
        nebulaeCount = 2

        for i in range(starsCount):
            self.backgroundElements.append(BackgroundElement("stars", 0, (-1344 + sh - i * 1344), sw, sh, self.backgroundElements))
        
        for i in range(nebulaeCount):
            self.backgroundElements.append(BackgroundElement("nebulae", 0, (-3201 + sh - i * 3201), sw, sh, self.backgroundElements))
        
        
    def render(self, screen, dt, sw, sh):
   
        self.timer += dt
        
        for backgroundElement in self.backgroundElements:
            elementSpeed = 0
            if backgroundElement.elementType == "stars":
                elementSpeed = 200
                if backgroundElement.y >= 672:
                    backgroundElement.y -= 2688 
            elif backgroundElement.elementType == "nebulae":
                elementSpeed = 150
                if backgroundElement.y >= 3201:
                    backgroundElement.y -= 6402 
            elif backgroundElement.elementType[:-1] == "planet":
                elementSpeed = 50
            backgroundElement.animate(elementSpeed, dt)
            backgroundElement.tick()
            backgroundElement.render(screen)

        if self.timer > self.planetSpawnCooldown:
            self.timer = 0
            doubleSpawn = random.randint(1,5)
            if doubleSpawn == 1:
                self.planetSpawnCooldown = random.randint(2, 4)
                self.spawnPlanet(sw, sh)
            else:
                self.planetSpawnCooldown = random.randint(8, 15)
                self.spawnPlanet(sw, sh)

    def spawnPlanet(self, sw, sh):
        planetNumber = random.randint(1,3)
        randomXPos = random.randint(20, sw-20)
        while abs(randomXPos-self.lastPlanetXPos) < 200:
            randomXPos = random.randint(20, sw-200)
        self.lastPlanetXPos = randomXPos

        planetToSpawn = BackgroundElement("planet" + str(planetNumber), randomXPos, -150, sw, sh, self.backgroundElements)
       
        planetSizeProportion = planetToSpawn.element_image.get_width() / planetToSpawn.element_image.get_height()
        randx = random.randint(100,200)
        size = (randx, randx / planetSizeProportion)
        planetToSpawn.element_image = pygame.transform.scale(planetToSpawn.element_image, size)
        


        self.backgroundElements.append(planetToSpawn)
        return randx

class BackgroundElement:
    def __init__(self, elementType, x, y, sw, sh, backgroundElements):
        self.elementType = elementType
        self.x = x
        self.y = y
        sprite = "sprites/" + str(elementType) + ".png"
        self.element_image = pygame.image.load(sprite)
        self.isOnTop = True
        
            
            

        

        # collidesWithAny = True
        # while collidesWithAny:
        #     collidesWithAny = False
        #     for otherElement in backgroundElements:
        #         if self.element_image.get_rect().colliderect(otherElement.element_rect):
        #             collidesWithAny = True
        #     if collidesWithAny:
        #         self.x = random.randint(0, sw)
        #         self.y = random.randint(0, sh)
        #         self.element_rect = self.element_image.get_rect()
        #         self.element_rect.x = self.x
        #         self.element_rect.y = self.y
                
        
        self.element_rect = self.element_image.get_rect()
        
    def tick(self):
        self.element_rect.x = self.x
        self.element_rect.y = self.y
        
    def animate(self, elementSpeed, dt):
        self.y += elementSpeed * dt
            
            
    def render(self, screen):
        screen.blit(self.element_image, self.element_rect)