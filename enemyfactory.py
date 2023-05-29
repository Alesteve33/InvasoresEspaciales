import pygame
import random
from enemy import Enemy
from enemyrow import EnemyRow
from boss import Boss

class EnemyFactory:

    def __init__(self, actualLevelRows, difficulty, player):
        self.currentLevelRows = 0
        self.actualLevelRows = actualLevelRows
        self.rowsLeft= 0
        self.player = player
        self.wavesSpawned = 1
        self.wavesForBoss = 1

        self.boss = None

        self.difficulty = difficulty

        #Herramienta de debug, no usar esto para juego normal. NORMAL-TRUE | DEBUG-FALSE
        self.keepSpawning = False


    def spawnBoss(self):
        self.boss = Boss(100, -220, 3, 10, 0, self.difficulty, self.player)

    def spawnCheck(self, enemyRows):
        if self.rowsLeft > 0 and self.keepSpawning:
            self.spawn(enemyRows)

    def spawnBossCheck(self, enemyRows):
        if self.wavesSpawned >= self.wavesForBoss and self.boss == None and len(enemyRows) == 0 and (self.rowsLeft < 1 or not self.keepSpawning):
            self.rowsLeft = 0
            self.spawnBoss()

        if not self.boss == None:
            self.rowsLeft = 0

    def spawnLines(self, minRows, maxRows):
        self.wavesSpawned += 1
        self.rowsLeft = random.randint(minRows, maxRows)

    def updateDifficulty(self, difficulty):
        self.difficulty = difficulty

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
