import pygame
import random
import math
from Animation import AnimationFrame, AnimationPlayer

class FlyingEnemy:
    def __init__(self, x, y, direction) -> None:
        self.position = pygame.Vector2(x, y)
        self.direction = 1
        self.distance = 20
        self.cooldown = 0
        self.hitbox = pygame.Rect(x, y, 50, 30)
        self.projectiles = []
        self.shotCooldown = 0
        self.health = 4
        self.animation = AnimationPlayer([AnimationFrame(pygame.image.load("./assets/flying enemy flap 1.png"), 30), AnimationFrame(pygame.image.load("./assets/flying enemy flap 2.png"), 30)])
    def changedirection(self):
        r = random.randint(1, 6)
        self.cooldown = random.randint(0, 300)
        if r not in [2, 4]:
            self.direction *= -1
        self.distance = random.randint(100, 800)
    def fly(self, platforms, player):
        if self.cooldown > 0:
            self.cooldown -= 1
        elif self.distance <= 0:
            self.changedirection()
        else:
            for platform in platforms:
                if platform.hitbox.colliderect(self.position.x + 1*self.direction, self.position.y, 50, 30):
                    self.direction *= -1
            self.position.x += 1 * self.direction
            self.distance -= 1
        
        # if the distance from the player is less than 450 px
        if math.hypot(player.position.y - self.position.y, player.position.x - self.position.x) < 450:
            if self.shotCooldown > 0:
                self.shotCooldown -= 1
            else:
                direction = player.position - self.position
                angle = math.atan2(direction.x, direction.y)
                self.projectiles.append(Projectile(self.position.x, self.position.y, angle))
                self.shotCooldown = 55
        
        for projectile in self.projectiles:
            projectile.move()
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
        self.sprite = pygame.image.load("assets/ground enemy.png")
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
            for index, platform in enumerate(platforms):
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
                    if random.randint(0, 480) == 2:
                        platform.dark = True
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
                    # collision with side of block
                    self.direction *= -1
        self.position.x += self.velocity.x * self.direction
        self.position.y += self.velocity.y
        self.hitbox = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    def render(self, screen, camera):
        screen.blit(self.sprite, (self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y))
        #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, self.size.x, self.size.y))


class Projectile:
    def __init__(self, x, y, angle):
        self.position = pygame.Vector2(x + 15, y + 20)
        self.angle = angle
        self.life = 60
    
    def move(self):
        self.position.x += 7 * math.sin(self.angle)
        self.position.y += 7 * math.cos(self.angle)
        self.life -= 1
    
    def draw(self, screen, camera):
        pygame.draw.circle(screen, "black", (
            self.position.x - camera.target.x + camera.offset.x + 15,
            self.position.y - camera.target.y + camera.offset.y + 20)
        , 5)
