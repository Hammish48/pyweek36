import pygame
import random

class FlyingEnemy:
    def __init__(self, x, y, direction) -> None:
        self.position = pygame.Vector2(x, y)
        self.direction = 1
        self.distance = 20
        self.cooldown = 0
        self.hitbox = pygame.Rect(x, y, 50, 30)
    def changedirection(self):
        r = random.randint(1, 6)
        self.cooldown = random.randint(0, 300)
        if r not in [2, 4]:
            self.direction *= -1
        self.distance = random.randint(100, 800)
    def fly(self, platforms):
        if self.cooldown > 0:
            self.cooldown -= 1
        elif self.distance <= 0:
            self.changedirection()
        else:
            self.position.x += 1 * self.direction
            self.distance -= 1
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 50, 30)