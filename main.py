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
from shield import Shield

pygame.init()
pygame.font.init()
pygame.mixer.init()

size = WIDTH, HEIGHT = 768, 672
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ship Killer")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("sprites/logo.png"), (32, 32)))

FPS = 60
clock = pygame.time.Clock()
dt = 0
timeToGoDown = 6
timeToSpawn = 1.5
timer = 0

enemiesAreSpawning = True

startAnimationTimer = 0
startAnimationTimeToGoDown = 0.5
isOnStartAnimation = False

enemyRows = []
bullets = []

background = Background(WIDTH, HEIGHT)


direction = 0

bulletRand = 96

font = pygame.font.SysFont('Comic Sans MS', 30)

menu = Menu(screen, WIDTH, HEIGHT, font)

fade = Fade()

stats = Stats(menu)
player = Player(WIDTH/2-80, 585, 250.0, 4, menu, stats)


pygame.mixer.music.load("sounds/music/menu1.mp3")
pygame.mixer.music.play(5)
shoot_sound = pygame.mixer.Sound("sounds/shoot.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
enemy_killed_sound = pygame.mixer.Sound("sounds/enemyKilled.mp3")

enemyFactory = EnemyFactory(random.randint(2, 5), menu.difficulty, player, explosion_sound)
enemyFactory.spawnLines(4, 6)
enemyFactory.spawnCheck(enemyRows)

running = True
while running:
    enemyFactory.updateDifficulty(menu.difficulty)

    

    shoot_sound.set_volume(menu.volume * 0.003)
    explosion_sound.set_volume(menu.volume * 0.002)
    enemy_killed_sound.set_volume(menu.volume * 0.001)
    menu.menu_select_sound.set_volume(menu.volume * 0.01)
    menu.game_over_sound.set_volume(menu.volume * 0.002)
    player.health_sound.set_volume(menu.volume * 0.003)
    player.shield.enableShieldSound.set_volume(menu.volume * 0.003)
    player.shield.disableShieldSound.set_volume(menu.volume * 0.003)

    if menu.musicOn:
        pygame.mixer.music.set_volume(menu.volume * 0.003)
    else:
        pygame.mixer.music.set_volume(0)

    if not menu.isInMenu:
        fade.tick()

    keys = pygame.key.get_pressed()

    if menu.isInMenu:
        
        if menu.difficulty == 0:
            player.shield.shieldMaxTime = 7.5
            player.shield.cooldown = 4.5
            player.shoot_cooldown = 0.35
            bulletRand = 98
        elif menu.difficulty == 1:
            player.shield.shieldMaxTime = 6
            player.shield.cooldown = 5
            player.shoot_cooldown = 0.375
            bulletRand = 96
        elif menu.difficulty == 2:
            player.shield.shieldMaxTime = 5
            player.shield.cooldown = 8
            player.shoot_cooldown = 0.4
            bulletRand = 90
        elif menu.difficulty == 3:
            player.shield.shieldMaxTime = 4
            player.shield.cooldown = 10
            player.shoot_cooldown = 0.45
            bulletRand = 80

        if not menu.isGameOver:
            player.score = 0
            player.timeAlive = 0

        menu.render(screen, font, player.score, player.timeAlive, dt, stats)
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

        player.shield.indicator.render(screen)

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
            enemiesAreSpawning = False
            enemyFactory.wavesSpawned = 1

        fade.render(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000

        keys = False
        pygame.event.clear()

        continue

    if player.isExploding:
        fade.setFadeState(2)

        screen.fill((5, 2, 25))
        background.render(screen, dt, WIDTH, HEIGHT)

        if player.finishedExplosion:
            menu.isInMenu = True
            menu.isGameOver = True

            player.shield = Shield()

            menu.game_over_sound.play()

            enemyFactory = EnemyFactory(random.randint(2, 5), menu.difficulty, player, explosion_sound)
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

        player.shield.indicator.render(screen)

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

    player.shield.indicator.render(screen)
    timer += dt

    if timer >= timeToGoDown and not enemiesAreSpawning and enemyFactory.boss == None:
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

    enemyFactory.spawnBossCheck(enemyRows)
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

    if not enemyRows and enemyFactory.rowsLeft <= 0 and enemyFactory.wavesSpawned < enemyFactory.wavesForBoss:
        enemyFactory.spawnLines(4, 6)
        timer = 0
        enemiesAreSpawning = False

    for enemyToRemove in removeEnemyList:
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if enemy == enemyToRemove:
                    enemyRow.enemies.remove(enemyToRemove)
                    player.addScore(1)
                if not enemyRow.enemies:
                    enemyRows.remove(enemyRow)

    for bullet in bullets:
        bullet.tick(dt)
        bullet.render(screen)

    if not enemyFactory.boss == None:
        enemyFactory.boss.doAi(bullets, player, dt)
        enemyFactory.boss.tick(dt, player, bullets)
        enemyFactory.boss.render(screen)

        if enemyFactory.boss.isDead:
            enemyFactory.boss = None
            enemyFactory.wavesSpawned = 0
    if not enemyRows and enemyFactory.rowsLeft > 0:
        enemiesAreSpawning = True


    pygame.display.update()
    dt = clock.tick(FPS) / 1000

pygame.quit()
