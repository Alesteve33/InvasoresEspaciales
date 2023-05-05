import pygame
from player import Player

class Menu:
    
    def __init__(self):
        self.isInMenu = True
        self.buttonSelected = 0
        self.buttonAmount = 3
        self.colors = []
        
        self.isGameOver = False
        
        for i in range(self.buttonAmount):
            self.colors.append((255,255,255))
    
        self.skull_image = pygame.transform.scale(pygame.image.load("sprites/skull.png"), (128, 128))
        self.skull_rect = self.skull_image.get_rect()
    
    def handleKey(self, keys, deltaTime, enemyRows, player, bullets, spawner):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.buttonSelected -= 1
                elif event.key == pygame.K_DOWN:
                    self.buttonSelected += 1
                elif event.key == pygame.K_RETURN:
                    if self.buttonSelected == 0: #PLAY
                        self.isInMenu = False
                    elif self.buttonSelected == 1: #SETTINGS
                        continue
                    else:
                        pygame.quit()
                        exit()
                elif event.key == pygame.K_SPACE:
                    if self.isGameOver:
                        enemyRows.clear()
                        bullets.clear()
                        #player = Player(100, 585, 250.0, 4)
                        player.health = 4
                        player.x = 100
                        spawner.spawnLines(4, 5)
                        self.isGameOver = False

            if self.buttonSelected >= self.buttonAmount:
                self.buttonSelected = 0
            elif self.buttonSelected < 0:
                self.buttonSelected = self.buttonAmount - 1
        
        return True            
    
    def render(self, screen, font):
        screen.fill((0,0,0))
        if self.isGameOver:
            self.skull_rect.x = screen.get_size()[0]/2 - 66
            self.skull_rect.y = screen.get_size()[1]/2 - 50
            
            screen.blit(self.skull_image, self.skull_rect)
            youDiedText = font.render("You died!", False, (255, 255, 255))
            screen.blit(youDiedText, (screen.get_size()[0]/2 - font.size("Ship Killer")[0]/2, screen.get_size()[1]/2 - 100))
            pressSpaceText = font.render("Press Space to continue", False, (255, 255, 255))
            screen.blit(pressSpaceText, (screen.get_size()[0]/2 - font.size("Press Space to continue")[0]/2, screen.get_size()[1]/2 + 80))
            return
        
        colorNotSelected = (255, 255, 255)
        colorSelected = (204, 255, 0)
        for i in range(self.buttonAmount):
            if self.buttonSelected == i:
                self.colors[i] = colorSelected
            else:
                self.colors[i] = colorNotSelected
        
        
        
        creditText = font.render("By Daniel Villena and Alejandro Vila", False, (200, 200, 200))
        screen.blit(creditText, (screen.get_size()[0]/2 - font.size("By Daniel Villena and Alejandro Vila")[0]/2, screen.get_size()[1]/2 - 120))
        
        
        playText = font.render("Play", False, self.colors[0])
        settingsText = font.render("Settings", False, self.colors[1])
        exitText = font.render("Exit", False, self.colors[2])
        
        titleText = font.render("Ship Killer", False, (200, 155, 45))
        
        screen.blit(titleText, (screen.get_size()[0]/2 - font.size("Ship Killer")[0]/2, screen.get_size()[1]/4))
        
        screen.blit(playText, (screen.get_size()[0]/2 - font.size("Play")[0]/2, screen.get_size()[1]/4 + 100))
        screen.blit(settingsText, (screen.get_size()[0]/2 - font.size("Settings")[0]/2, screen.get_size()[1]/4 + 200))
        screen.blit(exitText, (screen.get_size()[0]/2 - font.size("Exit")[0]/2, screen.get_size()[1]/4 + 300))
        