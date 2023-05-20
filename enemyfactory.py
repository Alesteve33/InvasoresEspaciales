import pygame
import random
from enemy import Enemy
from enemyrow import EnemyRow
from boss import Boss

class EnemyFactory:

    def __init__(self, actualLevelRows):
        self.currentLevelRows = 0
        self.actualLevelRows = actualLevelRows
        self.rowsLeft= 0

        self.rowsSpawned = 0
        self.rowsForBoss = 0

        self.boss = None

        #Herramienta de debug, no usar esto para juego normal. Debe estar en True si no estás debugeando el boss
        self.keepSpawning = True


    def spawnBoss(self):
        self.boss = Boss(100, -220, 3, 10, 20, 0)

    def spawnCheck(self, enemyRows):
        if self.rowsSpawned == self.rowsForBoss and self.boss == None and len(enemyRows) == 0:
            self.rowsLeft = 0
            self.spawnBoss()

        if not self.boss == None:
            self.rowsLeft = 0

        if self.rowsLeft > 0 and self.keepSpawning:
            self.spawn(enemyRows)
            self.rowsSpawned += 1

    def spawnLines(self, minRows, maxRows):
        self.rowsLeft = random.randint(minRows, maxRows)

    def spawn(self, enemyRows):
        if not self.keepSpawning:
            return
        direction = 0
        row_size = random.randint(4,7)
        self.rowsLeft -= 1
        if direction == 0:
            direction = 1
        else:
            direction = 0
        enemyRow = EnemyRow(direction)

        for j in range(row_size):
            enemy = Enemy (175 + j * (64 + 10), 64, 0, 100.0, 1, direction)
            enemyRow.enemies.append(enemy)
        enemyRows.append(enemyRow)
