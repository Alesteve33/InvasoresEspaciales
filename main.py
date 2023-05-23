import pygame
import random
import time
from player import Player
from enemy import Enemy
from bullet import Bullet
from enemyfactory import EnemyFactory
from menu import Menu
from background import Background
from fade import Fade
from stats import Stats
from boss import Boss

pygame.init()
pygame.font.init()
pygame.mixer.init()

size = WIDTH, HEIGHT = 768, 672
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ship Killer")

FPS = 60
clock = pygame.time.Clock()
dt = 0
timeToGoDown = 6
timeToSpawn = 1.5
timer = 0

enemiesAreSpawning = False

startAnimationTimer = 0
startAnimationTimeToGoDown = 0.5
isOnStartAnimation = False

enemyRows = []
bullets = []

background = Background(WIDTH, HEIGHT)

player = Player(WIDTH/2-80, 585, 250.0, 4)

direction = 0

bulletRand = 96

font = pygame.font.SysFont('Comic Sans MS', 30)
enemyFactory = EnemyFactory(random.randint(2, 5))
#enemyFactory.spawnLines(4, 4)
#enemyFactory.spawnCheck(enemyRows)

menu = Menu(screen, WIDTH, HEIGHT, font)

fade = Fade()

stats = Stats()


shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
enemy_killed_sound = pygame.mixer.Sound("sounds/enemyKilled.mp3")

running = True
while running:

    shoot_sound.set_volume(menu.volume * 0.01)
    explosion_sound.set_volume(menu.volume * 0.01)
    enemy_killed_sound.set_volume(menu.volume * 0.01)
    menu.menu_select_sound.set_volume(menu.volume * 0.01)
    menu.game_over_sound.set_volume(menu.volume * 0.01)
    player.health_sound.set_volume(menu.volume * 0.01)
    player.shield.enableShieldSound.set_volume(menu.volume * 0.01)
    player.shield.disableShieldSound.set_volume(menu.volume * 0.01)

    if not menu.isInMenu:
        fade.tick()

    keys = pygame.key.get_pressed()

    if menu.isInMenu:
        if not menu.isGameOver:
            player.score = 0

        menu.render(screen, font, player.score, dt, stats)
        handleKeys = menu.handleKey(keys, dt, enemyRows, player, bullets, enemyFactory)
        if not handleKeys:
            running = False
        elif handleKeys:
            isOnStartAnimation = True

        pygame.display.update()
        dt = clock.tick(FPS) / 1000
        keys = False
        continue

    if isOnStartAnimation and enemyFactory.keepSpawning:
        fade.setFadeState(1)

        startAnimationTimer += dt
        screen.fill((5, 2, 25))

        background.render(screen, dt, WIDTH, HEIGHT)
        player.render(screen, dt)

        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                enemy.canShoot = False
                lastEnemyInRow = enemyRow.enemies[len(enemyRow.enemies) - 1]
                firstEnemyInRow = enemyRow.enemies[0]

                if lastEnemyInRow.direction == 0:
                    enemy.x += enemy.speed * dt
                else:
                    enemy.x -= enemy.speed * dt

                if lastEnemyInRow.x > size[0] - lastEnemyInRow.size[0]:
                    enemy.direction = 1
                elif firstEnemyInRow.x < 0:
                    enemy.direction = 0

                enemy.tick(bullets, player.x, player.y, dt, bulletRand)
                enemy.render(screen)
        for bullet in bullets:
            bullet.tick(dt)
            bullet.render(screen)


        scoreText = font.render("Score: " + str(player.score), False, (255, 255, 255))
        screen.blit(scoreText, (0, 0))

        if startAnimationTimer >= startAnimationTimeToGoDown and enemyFactory.rowsLeft > 0:
            startAnimationTimer = 0
            for enemyRow in enemyRows:
                for enemy in enemyRow.enemies:
                    enemy.y += enemy.size[1] + 20
            enemyFactory.spawnCheck(enemyRows)

        elif enemyFactory.rowsLeft <= 0:
            for enemyRow in enemyRows:
                for enemy in enemyRow.enemies:
                    enemy.canShoot = True
            isOnStartAnimation = False

        fade.render(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000

        keys = False

        continue

    if player.isExploding:
        fade.setFadeState(2)

        screen.fill((5, 2, 25))
        background.render(screen, dt, WIDTH, HEIGHT)

        if player.finishedExplosion:
            menu.isInMenu = True
            menu.isGameOver = True

            menu.game_over_sound.play()

            enemyFactory = EnemyFactory(random.randint(2, 5))
            enemyFactory.spawnLines(4, 4)
            enemyFactory.spawnCheck(enemyRows)

            stats.deaths += 1
            if player.score > stats.highScore:
                stats.highScore = player.score

        for bullet in bullets:
            bullet.tick(dt)
            bullet.render(screen)
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                lastEnemyInRow = enemyRow.enemies[len(enemyRow.enemies) - 1]
                firstEnemyInRow = enemyRow.enemies[0]

                if lastEnemyInRow.direction == 0:
                    enemy.x += enemy.speed * dt
                else:
                    enemy.x -= enemy.speed * dt

                if lastEnemyInRow.x > size[0] - lastEnemyInRow.size[0]:
                    enemy.direction = 1
                elif firstEnemyInRow.x < 0:
                    enemy.direction = 0

                enemy.tick(bullets, player.x, player.y, dt, bulletRand)
                enemy.render(screen)
        player.render(screen, dt)

        if not enemyFactory.boss == None:
            enemyFactory.boss.tick(dt, player, bullets)
            enemyFactory.boss.render(screen)

        fade.render(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000
        keys = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not menu.holdShoot:
                b = player.shoot()
                if b is not None:
                    bullets.append(b)
                    shoot_sound.play()
            if event.key == pygame.K_ESCAPE and not menu.isInMenu and not isOnStartAnimation:
                player.isExploding = True
                explosion_sound.play()

    if keys[pygame.K_SPACE] and menu.holdShoot:
        b = player.shoot()
        if b is not None:
            bullets.append(b)
            shoot_sound.play()

    screen.fill((5, 2, 25))

    background.render(screen, dt, WIDTH, HEIGHT)

    scoreText = font.render("Score: " + str(player.score), False, (255, 255, 255))
    screen.blit(scoreText, (0, 0))

    player.handleKey(keys, dt)
    if not player.tick(dt, bullets):
        player.isExploding = True
        explosion_sound.play()

    player.render(screen, dt)

    timer += dt

    if timer >= timeToGoDown and not enemiesAreSpawning:
        timer = 0
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if not enemy.y > player.y:
                    enemy.y += enemy.size[1] + 20
        enemyFactory.spawnCheck(enemyRows)
    elif enemiesAreSpawning and timer >= timeToSpawn:
        timer = 0
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if not enemy.y > player.y:
                    enemy.y += enemy.size[1] + 20
        enemyFactory.spawnCheck(enemyRows)
        if enemyFactory.rowsLeft <= 0:
            enemiesAreSpawning = False
    
    enemyFactory.spawnCheck(enemyRows)
    removeEnemyList = []
    for enemyRow in enemyRows:
        for enemy in enemyRow.enemies:
            lastEnemyInRow = enemyRow.enemies[len(enemyRow.enemies) - 1]
            firstEnemyInRow = enemyRow.enemies[0]

            if lastEnemyInRow.direction == 0:
                enemy.x += enemy.speed * dt
            else:
                enemy.x -= enemy.speed * dt

            if lastEnemyInRow.x > size[0] - lastEnemyInRow.size[0]:
                #lastEnemyInRow.direction = 1
                enemy.direction = 1
                #enemy.y += enemy.size[1] + 20
            elif firstEnemyInRow.x < 0:
                #lastEnemyInRow.direction = 0
                enemy.direction = 0
                #enemy.y += enemy.size[1] + 20

            if enemy.enemy_rect.colliderect(player.player_rect):
                player.health = 0
                enemy.health = 0

            enemy.tick(bullets, player.x, player.y, dt, bulletRand)
            enemy.render(screen)
            if enemy.health <= 0:
                removeEnemyList.append(enemy)
                stats.kills += 1

                enemy_killed_sound.play()

    #if not enemyRows and enemyFactory.rowsLeft <= 0:
    #    enemyFactory.spawnLines(4, 4)
    #    timer = 0
    #    enemiesAreSpawning = True

    for enemyToRemove in removeEnemyList:
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if enemy == enemyToRemove:
                    enemyRow.enemies.remove(enemyToRemove)
                    player.score += 1
                    stats.totalScore += 1
                if not enemyRow.enemies:
                    enemyRows.remove(enemyRow)

    for bullet in bullets:
        bullet.tick(dt)
        bullet.render(screen)

    if not enemyFactory.boss == None:
        enemyFactory.boss.doAi(bullets, player, dt)
        enemyFactory.boss.tick(dt, player, bullets)
        enemyFactory.boss.render(screen)

        if enemyFactory.boss.finishedExplosion:
            enemyFactory.boss = None
            enemyFactory.rowsSpawned = 0
            
    pygame.display.update()
    dt = clock.tick(FPS) / 1000

pygame.quit()
