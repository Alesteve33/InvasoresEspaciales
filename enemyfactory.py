import pygame
import random
from enemy import Enemy
from enemyrow import EnemyRow

class EnemyFactory:

    def __init__(self, actualLevelRows):
        self.currentLevelRows = 0
        self.actualLevelRows = actualLevelRows
        self.rowsLeft= 0

        #Herramienta de debug, no usar esto para juego normal. Debe estar en True si no estás debugeando el boss
        self.keepSpawning = False


    def spawnCheck(self, enemyRows):
        if self.rowsLeft > 0 and self.keepSpawning:
            self.spawn(enemyRows)

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
