import pygame
from player import Player

class Menu:

    def __init__(self, screen, sw, sh, font):
        self.isInMenu = True
        self.buttonSelected = 0
        self.buttonAmount = 4
        self.colors = []

        self.isInSettings = False
        self.isGameOver = False
        self.isInStats = False

        self.holdShoot = True
        self.volume = 50
        self.musicOn = True

        self.volumeCooldown = 0.1
        self.volumeTimer = 0

        self.screen = screen
        self.sw = sw
        self.sh = sh

        self.menu_select_sound = pygame.mixer.Sound("sounds/menuSelect.mp3")

        for i in range(self.buttonAmount):
            self.colors.append((255,255,255))

        self.skull_image = pygame.transform.scale(pygame.image.load("sprites/skull.png"), (128, 128))
        self.skull_rect = self.skull_image.get_rect()

        self.arrow_image = pygame.transform.scale(pygame.image.load("sprites/arrow.png"), (32, 32))
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.x = self.sw/2 - font.size("Volume: " + str(self.volume) + "%")[0]/2 - 50
        self.arrow_rect.y = self.sh/4 + 155


        self.arrow_2_image = pygame.transform.rotate(self.arrow_image, 180)
        self.arrow_2_rect = self.arrow_2_image.get_rect()
        self.arrow_2_rect.x = self.sw/2 - font.size("Volume: " + str(self.volume) + "%")[0]/2 + 195
        self.arrow_2_rect.y = self.sh/4 + 155

    def handleKey(self, keys, deltaTime, enemyRows, player, bullets, spawner):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP and not self.isGameOver):
                    self.buttonSelected -= 1
                    self.menu_select_sound.play()
                elif (event.key == pygame.K_DOWN and not self.isGameOver):
                    self.buttonSelected += 1
                    self.menu_select_sound.play()
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and not self.isGameOver:
                    self.menu_select_sound.play()
                    if not self.isInSettings:
                        if self.buttonSelected == 0: #PLAY
                            self.isInMenu = False
                            return True
                        elif self.buttonSelected == 1: #SETTINGS:
                            self.isInSettings = True
                            continue
                        elif self.buttonSelected == 2: #STATS
                            self.isInStats = True
                            continue
                        else:
                            pygame.quit()
                            exit()
                    if self.isInSettings and self.buttonSelected == 0:
                        self.holdShoot = not self.holdShoot
                    elif self.isInSettings and self.buttonSelected == 2:
                        self.musicOn = not self.musicOn
                    elif self.isInSettings and self.buttonSelected == 3:
                        self.isInSettings = False
                        self.buttonSelected = 1

                elif event.key == pygame.K_ESCAPE:
                    if self.isInSettings:
                        self.isInSettings = False
                        self.buttonSelected = 1
                    if self.isInStats:
                        self.isInStats = False
                        self.buttonSelected = 2
                elif event.key == pygame.K_SPACE:
                    if self.isGameOver:
                        enemyRows.clear()
                        bullets.clear()
                        #player = Player(100, 585, 250.0, 4)
                        player.health = 4
                        player.x = 304
                        player.currentAnimationFrame = 0
                        player.isExploding = False
                        player.finishedExplosion = False
                        player.tick(deltaTime, bullets)
                        spawner.spawnLines(4, 5)
                        self.isGameOver = False


        return True

    def render(self, screen, font, score, dt, stats):
        keys = pygame.key.get_pressed()
        self.volumeTimer += dt
        if self.volumeTimer > self.volumeCooldown and self.buttonSelected == 1:
            if keys[pygame.K_LEFT]:
                self.volumeTimer = 0
                if self.isInSettings and self.volume > 0:
                    self.menu_select_sound.play()
                    self.volume -= 1
            elif keys[pygame.K_RIGHT]:
                self.volumeTimer = 0
                if self.isInSettings and self.volume < 100:
                    self.menu_select_sound.play()
                    self.volume += 1

        if self.buttonSelected >= self.buttonAmount:
            self.buttonSelected = 0
        elif self.buttonSelected < 0:
            self.buttonSelected = self.buttonAmount - 1


        screen.fill((0,0,0))
        if self.isInSettings:
            settingsText = font.render("Settings", False, (255, 155, 155))
            screen.blit(settingsText, (screen.get_size()[0]/2 - font.size("Settings")[0]/2, screen.get_size()[1]/2 - 200))

            toggleAttackText = "ON"
            if not self.holdShoot:
                toggleAttackText = "OFF"

            toggleMusicText = "ON"
            if not self.musicOn:
                toggleMusicText = "OFF"

            holdAttackText = font.render("Hold attack: " + toggleAttackText , False, self.colors[0])
            volumeText = font.render("Volume: " + str(self.volume) + "%", False, self.colors[1])
            musicText = font.render("Music: " + toggleMusicText, False, self.colors[2])
            exitText = font.render("Go back", False, self.colors[3])

            titleText = font.render("Ship Killer", False, (200, 155, 45))

            screen.blit(holdAttackText, (screen.get_size()[0]/2 - font.size("Hold attack: " + toggleAttackText)[0]/2, screen.get_size()[1]/4 + 50))
            screen.blit(volumeText, (screen.get_size()[0]/2 - font.size("Volume: " + str(self.volume) + "%")[0]/2, screen.get_size()[1]/4 + 150))
            screen.blit(musicText, (screen.get_size()[0]/2 - font.size("Music: " + toggleMusicText)[0]/2, screen.get_size()[1]/4 + 250))
            screen.blit(exitText, (screen.get_size()[0]/2 - font.size("Go back")[0]/2, screen.get_size()[1]/4 + 350))

            screen.blit(self.arrow_image, self.arrow_rect)
            screen.blit(self.arrow_2_image, self.arrow_2_rect)

        if self.isInStats:
            statsText = font.render("Statistics", False, (255, 155, 155))
            screen.blit(statsText, (screen.get_size()[0]/2 - font.size("Statistics")[0]/2, screen.get_size()[1]/2 - 180))

            killsText = font.render("Kills: " + str(stats.kills), False, (255, 255, 255))
            screen.blit(killsText, (screen.get_size()[0]/2 - font.size("Kills: " + str(stats.kills))[0]/2, screen.get_size()[1]/2 - 100))

            deathsText = font.render("Deaths: " + str(stats.deaths), False, (255, 255, 255))
            screen.blit(deathsText, (screen.get_size()[0]/2 - font.size("Deaths: " + str(stats.deaths))[0]/2, screen.get_size()[1]/2 - 60))

            totalScoreText = font.render("Total score: " + str(stats.totalScore), False, (255, 255, 255))
            screen.blit(totalScoreText, (screen.get_size()[0]/2 - font.size("Total score: " + str(stats.totalScore))[0]/2, screen.get_size()[1]/2 - 20))

            highScoreText = font.render("Highscore: " + str(stats.highScore), False, (255, 255, 255))
            screen.blit(highScoreText, (screen.get_size()[0]/2 - font.size("Highscore: " + str(stats.highScore))[0]/2, screen.get_size()[1]/2 + 20))

            goBackText = font.render("Press 'ESC' to go back!", False, (155, 155, 155))
            screen.blit(goBackText, (screen.get_size()[0]/2 - font.size("Press 'ESC' to go back!")[0]/2, screen.get_size()[1]/2 + 100))

            return

        if self.isGameOver:
            self.skull_rect.x = screen.get_size()[0]/2 - 66
            self.skull_rect.y = screen.get_size()[1]/2 - 50

            screen.blit(self.skull_image, self.skull_rect)
            youDiedText = font.render("You died!", False, (255, 30, 30))
            screen.blit(youDiedText, (screen.get_size()[0]/2 - font.size("You died!")[0]/2, screen.get_size()[1]/2 - 140))

            scoreText = font.render("Score: " + str(score), False, (255, 255, 255))
            screen.blit(scoreText, (screen.get_size()[0]/2 - font.size("Score: " + str(score))[0]/2, screen.get_size()[1]/2 - 100))

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

        if self.isInSettings:
            return
        creditText = font.render("By Daniel Villena and Alejandro Vila", False, (200, 200, 200))
        screen.blit(creditText, (screen.get_size()[0]/2 - font.size("By Daniel Villena and Alejandro Vila")[0]/2, screen.get_size()[1]/2 - 120))


        playText = font.render("Play", False, self.colors[0])
        settingsText = font.render("Settings", False, self.colors[1])
        statsText = font.render("Statistics", False, self.colors[2])
        exitText = font.render("Exit", False, self.colors[3])

        titleText = font.render("Ship Killer", False, (200, 155, 45))

        screen.blit(titleText, (screen.get_size()[0]/2 - font.size("Ship Killer")[0]/2, screen.get_size()[1]/4))

        screen.blit(playText, (screen.get_size()[0]/2 - font.size("Play")[0]/2, screen.get_size()[1]/4 + 100))
        screen.blit(settingsText, (screen.get_size()[0]/2 - font.size("Settings")[0]/2, screen.get_size()[1]/4 + 200))
        screen.blit(statsText, (screen.get_size()[0]/2 - font.size("Statistics")[0]/2, screen.get_size()[1]/4 + 300))
        screen.blit(exitText, (screen.get_size()[0]/2 - font.size("Exit")[0]/2, screen.get_size()[1]/4 + 400))
