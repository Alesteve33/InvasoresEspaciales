import pygame
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from enemyfactory import EnemyFactory
from menu import Menu
from background import Background

pygame.init()
pygame.font.init()

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
score = 0

direction = 0

bulletRand = 96

menu = Menu()

font = pygame.font.SysFont('Comic Sans MS', 30)
enemyFactory = EnemyFactory(random.randint(2, 5))
enemyFactory.spawnLines(4, 5)
enemyFactory.spawnCheck(enemyRows)

running = True
while running:
    
    keys = pygame.key.get_pressed()
    
    if menu.isInMenu:
        menu.render(screen, font)
        handleKeys = menu.handleKey(keys, dt, enemyRows, player, bullets, enemyFactory)
        if not handleKeys:
            running = False
        elif handleKeys:
            isOnStartAnimation = True

        pygame.display.update()
        dt = clock.tick(FPS) / 1000
        continue

    if isOnStartAnimation:
        startAnimationTimer += dt
        screen.fill((5, 2, 25))

        background.render(screen, dt, WIDTH, HEIGHT)
        player.render(screen)

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

        pygame.display.update()        
        dt = clock.tick(FPS) / 1000
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(keys[pygame.K_SPACE])
                b = player.shoot()
                if b is not None:
                    bullets.append(b)
            
    screen.fill((5, 2, 25))

    background.render(screen, dt, WIDTH, HEIGHT)
    
    scoreText = font.render("Score: " + str(score), False, (255, 255, 255))
    screen.blit(scoreText, (0, 0))
    
    player.handleKey(keys, dt)
    if not player.tick(dt, bullets):
        menu.isInMenu = True
        menu.isGameOver = True
    player.render(screen)

    timer += dt

    if timer >= timeToGoDown and not enemiesAreSpawning:
        timer = 0
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                enemy.y += enemy.size[1] + 20
        enemyFactory.spawnCheck(enemyRows)
    elif enemiesAreSpawning and timer >= timeToSpawn:
        timer = 0
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                enemy.y += enemy.size[1] + 20
        enemyFactory.spawnCheck(enemyRows)
        if enemyFactory.rowsLeft <= 0:
            enemiesAreSpawning = False


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
            
            
            enemy.tick(bullets, player.x, player.y, dt, bulletRand)
            enemy.render(screen)
            if enemy.health <= 0:
                removeEnemyList.append(enemy)

    if not enemyRows and enemyFactory.rowsLeft <= 0:
        enemyFactory.spawnLines(4, 5)
        timer = 0
        enemiesAreSpawning = True

    for enemyToRemove in removeEnemyList:
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if enemy == enemyToRemove:
                    enemyRow.enemies.remove(enemyToRemove)
                    score += 1
                if not enemyRow.enemies:
                    enemyRows.remove(enemyRow)
    
    for bullet in bullets:
        bullet.tick(dt)
        bullet.render(screen)
    
    pygame.display.update() 
    dt = clock.tick(FPS) / 1000
    
pygame.quit()