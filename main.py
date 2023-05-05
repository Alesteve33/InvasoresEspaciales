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

timeToGoDown = 7
timer = 0

enemyRows = []
bullets = []

background = Background(WIDTH, HEIGHT)

player = Player(100, 585, 250.0, 4)
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
        if not menu.handleKey(keys, dt, enemyRows, player, bullets, enemyFactory):
            running = False
        pygame.display.update()
        dt = clock.tick(FPS) / 1000
        continue
   
    enemyFactory.tick(dt)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if keys[pygame.K_SPACE]:
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

    if timer >= timeToGoDown:
        timer = 0
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                
                enemy.y += enemy.size[1] + 20
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
            
            
            enemy.tick(bullets, player.x, player.y, dt, bulletRand)
            enemy.render(screen)
            if enemy.health <= 0:
                removeEnemyList.append(enemy)
    
    for enemyToRemove in removeEnemyList:
        for enemyRow in enemyRows:
            for enemy in enemyRow.enemies:
                if enemy == enemyToRemove:
                    enemyRow.enemies.remove(enemyToRemove)
                    score += 1
    
    for bullet in bullets:
        bullet.tick(dt)
        bullet.render(screen)
    
    pygame.display.update() 
    dt = clock.tick(FPS) / 1000
    
pygame.quit()