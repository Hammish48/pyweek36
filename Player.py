import pygame
import math
from Animation import AnimationFrame, AnimationPlayer

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(1120/2, 580/2)
        self.velocity = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 50)
        self.onFloor = False
        self.forward = True
        self.bullets = []
        self.shoot_cooldown = 0  # Initialize the cooldown timer to 0
        self.shoot_cooldown_duration = 30
        self.animation = AnimationPlayer([AnimationFrame(pygame.image.load("assets/player/walk 1.png"), 10), AnimationFrame(pygame.image.load("assets/player/walk 2.png"), 3), AnimationFrame(pygame.image.load("assets/player/walk 3.png"), 4), AnimationFrame(pygame.image.load("assets/player/walk 4.png"), 6), AnimationFrame(pygame.image.load("assets/player/walk 5.png"), 6)])
        self.alive = True
        self.hitbox = pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y, self.size.x, self.size.y)
        self.health = 100
        self.end = pygame.Vector2(1,1)
        self.angle = 0
    
    def physicsProcess(self, platforms):
        self.velocity.x = 0
        if pygame.key.get_pressed()[pygame.K_a]:
            self.velocity.x -= 5
            self.animation.tick()
            self.forward = False
            
        if pygame.key.get_pressed()[pygame.K_d]:
            self.velocity.x += 5
            self.animation.tick()
            self.forward = True
            
        if not self.onFloor:
            self.velocity.y += 0.5 
        elif pygame.key.get_pressed()[pygame.K_w]:
            self.onFloor = False
            self.velocity.y = -15

        if self.onFloor:
            self.onFloor = False
            for platform in platforms:
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
        
        self.hitbox = pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y, self.size.x, self.size.y)

        # physics engine :DDDDDDD :)
        # the voices are getting louder
        for platform in platforms:
            # if player on next tick is in collision with platform
            if self.hitbox.colliderect(platform.hitbox):
                if self.position.x + self.size.x > platform.position.x and self.position.x < platform.position.x + platform.size.x:
                    # collision with top or bottom of player
                    self.velocity.y = 0
                    if self.position.y < platform.position.y:
                        self.position.y = platform.position.y - self.size.y
                        self.onFloor = True
                    elif self.position.y > platform.position.y + platform.size.y - 3:
                        self.position.y = platform.position.y + platform.size.y

                if self.position.y + self.size.y > platform.position.y and self.position.y < platform.position.y + platform.size.y:
                    # collision with side of player
                    self.velocity.x = 0
                    if self.position.x < platform.position.x:
                        self.position.x = platform.position.x - self.size.x
                    else:
                        self.position.x = platform.position.x + platform.size.x

        self.position += self.velocity

        if self.velocity.y > 50:
            self.alive = False

    def render(self, screen, platforms, camera, enemies):
        # pygame.draw.rect(screen, (0, 200, 20), pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, self.size.x, self.size.y))
        if self.onFloor:
            if self.forward:
                screen.blit(self.animation.getCurrentFrame(), self.position - camera.target + camera.offset)
            else:
                screen.blit(pygame.transform.flip(self.animation.getCurrentFrame(), True, False), self.position - camera.target + camera.offset)
        else:
            if self.forward:
                screen.blit(pygame.image.load("./assets/player/jump.png"), self.position - camera.target + camera.offset)
            else:
                screen.blit(pygame.transform.flip(pygame.image.load("./assets/player/jump.png"), True, False), self.position - camera.target + camera.offset)

        # get pos of hand on player
        hand_pos = pygame.math.Vector2(
            self.position.x - camera.target.x + camera.offset.x + self.size.x - self.size.x/2, 
            self.position.y - camera.target.y + camera.offset.y + self.size.y-30
        )

        # get cursor pos
        cursor = pygame.math.Vector2(pygame.mouse.get_pos())
        direction = cursor - hand_pos

        if direction.x != 0 or direction.y != 0:
            direction.normalize_ip()
        
        if (self.forward and math.atan2(direction.x, direction.y) > 0) or (not self.forward and math.atan2(direction.x, direction.y) < 0):
            self.angle = math.atan2(direction.x, direction.y)
            self.end = hand_pos + direction * 30
        else:
            self.forward = not self.forward

        end = hand_pos + direction * 30
        angle = math.atan2(direction.x, direction.y)
            
        pygame.draw.line(screen, "black", hand_pos, end, 14)


        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown == 0:
            self.bullets.append(Bullet(self.position.x + direction.x, self.position.y + direction.y, angle))
            self.shoot_cooldown = self.shoot_cooldown_duration
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1  # Decrement the cooldown timer

        for index, bullet in enumerate(self.bullets):
            if bullet.life < 0:
                self.bullets.pop(index)
            for platform in platforms:
                if platform.hitbox.collidepoint(bullet.position):
                    self.bullets.pop(index)
            for index, enemy in enumerate(enemies):
                if enemy.hitbox.collidepoint(bullet.position):
                    enemy.health -= 1
                    if enemy.health < 0:
                        enemies.pop(index)
                        print("ded enemy")
            bullet.move()
            bullet.draw(screen, camera)


class Bullet:
    def __init__(self, x, y, angle):
        self.position = pygame.Vector2(x, y)
        self.angle = angle
        self.life = 60
    
    def move(self):
        self.position.x += 25 * math.sin(self.angle)
        self.position.y += 25 * math.cos(self.angle)
        self.life -= 1
    
    def draw(self, screen, camera):
        pygame.draw.circle(screen, "black", (
            self.position.x - camera.target.x + camera.offset.x + 15,
            self.position.y - camera.target.y + camera.offset.y + 20)
        , 5)