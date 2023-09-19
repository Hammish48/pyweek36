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




class GroundEnemy:
    def __init__(self, x, y) -> None:
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(40, 40)
        self.velocity = pygame.Vector2(2, 0)
        self.onFloor = False
        self.distance = 20
        self.cooldown = 0
        self.direction = 1
        self.hitbox = pygame.Rect(x, y, self.size.x, self.size.y)
        self.health = 3
    def changedirection(self):
        self.cooldown = random.randint(0, 300)
        if random.randint(1, 6) < 2:
            self.direction *= -1
        self.distance = random.randint(100, 800)
    def move(self, platforms):
        if self.cooldown > 0:
            self.velocity.x = 0
            self.cooldown -= 1
        elif self.distance <= 0:
            self.changedirection()
            self.velocity.x = 0
        else:
            self.velocity.x = 2
            self.distance -= 1
        
        if not self.onFloor:
            self.velocity.y += 0.5 
        if self.onFloor:
            self.onFloor = False
            for platform in platforms:
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
        for platform in platforms:
            if pygame.Rect(self.position.x + (self.velocity.x * self.direction), self.position.y + self.velocity.y, self.size.x, self.size.y).colliderect(platform.hitbox):
                if self.position.x + self.size.x > platform.position.x and self.position.x < platform.position.x + platform.size.x:
                    # collision with top or bottom of enemy
                    self.velocity.y = 0
                    if self.position.y < platform.position.y:
                        self.position.y = platform.position.y - self.size.y
                        self.onFloor = True
                    elif self.position.y > platform.position.y + platform.size.y - 3:
                        self.position.y = platform.position.y + platform.size.y

                if self.position.y + self.size.y > platform.position.y and self.position.y < platform.position.y + platform.size.y:
                    # collision with side of player
                    self.direction *= -1
        self.position.x += self.velocity.x * self.direction
        self.position.y += self.velocity.y
        self.hitbox = pygame.Rect(self.position.x, self.position.x, self.size.x, self.size.y)
    def render(self, screen, camera):
        pygame.draw.rect(screen, (255, 255, 20), pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, self.size.x, self.size.y))
