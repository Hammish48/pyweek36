import pygame
import math
from Animation import AnimationFrame, AnimationPlayer

from pygame.locals import *

from pygame.sprite import Group
from Animation import AnimationFrame, AnimationPlayer

from pygame import mixer
mixer.init()
explosion_fx = pygame.mixer.Sound("assets\shoot\shoot.wav")


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        explosion_fx.play()
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"assets/shoot/{num}.png")
            pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()


class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(50, 20)
        self.velocity = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 50)
        self.onFloor = False
        self.forward = True
        self.bullets = []
        self.shoot_cooldown = 0  # Initialize the cooldown timer to 0
        self.shoot_cooldown_duration = 30
        self.animation = AnimationPlayer([AnimationFrame(pygame.image.load("assets/player/walk 1.png").convert_alpha(), 10), AnimationFrame(pygame.image.load("assets/player/walk 2.png").convert_alpha(), 3), AnimationFrame(pygame.image.load("assets/player/walk 3.png").convert_alpha(), 4), AnimationFrame(pygame.image.load("assets/player/walk 4.png").convert_alpha(), 6), AnimationFrame(pygame.image.load("assets/player/walk 5.png").convert_alpha(), 6)])
        self.alive = True
        self.hitbox = pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y, self.size.x, self.size.y)
        self.health = 100
        self.end = pygame.Vector2(1,1)
        self.angle = 0
        self.tip = 0
        self.infection = 0
        self.infection_rate = 0.01
        self.gun = Gun(0, 10, 30, "white", 2, 30, 1)
    
    def physicsProcess(self, platforms, enemies, camera, flyingEnemies, cures, healthboosts):
        self.velocity.x = 0
        
        if self.infection > 70:
            self.health -= 0.2

        for index, cure in enumerate(cures):
            if self.hitbox.colliderect(cure.hitbox):
                cures.pop(index)
                if self.infection > 30:
                    self.infection -= 30
                else:
                    self.infection = 0
        for index, boost in enumerate(healthboosts):
            if self.hitbox.colliderect(boost.hitbox):
                healthboosts.pop(index)
                if self.health < 60:
                    self.health += 40
                else:
                    self.health = 100

        # user Input
        if pygame.mouse.get_pressed()[0] and self.gun.cooldown == 0:
            self.gun.shoot(self.bullets)
        if self.gun.cooldown > 0:
            self.gun.cooldown -= 1  # Decrement the cooldown timer

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
                    if platform.dark:
                        self.infection_rate = 0.3
                    else:
                        self.infection_rate = 0.01
        
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
        self.infection += self.infection_rate
        if self.infection > 100:
            self.infection = 100

        self.position += self.velocity

        if self.velocity.y > 100:
            self.alive = False

        self.gun.physics(self.position, camera)
        if self.gun.angle > 0:
            self.forward = True
        else:
            self.forward = False
        self.gun.check_bullet_collisions(self.bullets, platforms, enemies, flyingEnemies, camera)
        

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

        self.gun.render(screen, camera)

        for bullet in self.bullets:
            bullet.render(screen, camera)


class Gun:
    def __init__(self, type = 0, cooldown_time = 30, bullet_life = 60, color = "red", bullet_size = 5, bullet_speed = 25, bullet_damage = 1):
        self.player_pos = pygame.Vector2(0, 0)
        self.type = type
        self.cursor_pos = pygame.mouse.get_pos()
        self.tip = (0, 0)
        self.angle = 0
        self.cooldown = 30
        self.cooldown_time = cooldown_time
        self.bullet_life = bullet_life
        self.color = color
        self.bullet_size = bullet_size
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage

    def physics(self, player_pos, camera):
        self.player_pos = player_pos
        pos = pygame.math.Vector2(
            player_pos.x - camera.target.x + camera.offset.x + 15, 
            player_pos.y - camera.target.y + camera.offset.y + 20
        )
        cursor = pygame.mouse.get_pos()
        direction = cursor - pos

        if direction != (0, 0):
            direction.normalize_ip()

        self.tip = pos + direction * 30
        self.angle = math.atan2(direction.x, direction.y)
    
    def check_bullet_collisions(self, bullets, platforms, enemies, flyingEnemies, camera):
        hit = False
        for indx, bullet in enumerate(bullets):
            pos = bullet.position
            if bullet.life < 0:
                bullets.pop(indx)
                break
            for platform in platforms:
                if platform.hitbox.collidepoint(bullet.position):
                    hit = bullet.position
                    bullets.pop(indx)
                    explosion = Explosion(pos.x - camera.target.x + camera.offset.x, pos.y - camera.target.y + camera.offset.y)
                    explosion_group.add(explosion)
                    break
            for index, enemy in enumerate(enemies):
                if enemy.hitbox.collidepoint(bullet.position):
                    enemy.health -= self.bullet_damage
                    if enemy.health < 0:
                        enemies.pop(index)
                    bullets.pop(indx)
                    explosion = Explosion(pos.x - camera.target.x + camera.offset.x, pos.y - camera.target.y + camera.offset.y)
                    explosion_group.add(explosion)
                    break
            for index, enemy in enumerate(flyingEnemies):
                if enemy.hitbox.collidepoint(bullet.position):
                    enemy.health -= self.bullet_damage
                    if enemy.health <= 0:
                        flyingEnemies.pop(index)
                    bullets.pop(indx)
                    explosion = Explosion(pos.x - camera.target.x + camera.offset.x, pos.y - camera.target.y + camera.offset.y)
                    explosion_group.add(explosion)
                    break
            bullet.move()
        if hit != False:
            for platform in platforms:
                if platform.dark:
                    if math.hypot(platform.position.y - hit.y, platform.position.x - hit.x) < 150:
                        platform.dark = False


    def shoot(self, bullets):
        bullets.append(Bullet(self.player_pos.x, self.player_pos.y, self.angle, self.bullet_life, self.bullet_speed, self.color, self.bullet_size))
        self.cooldown = self.cooldown_time
    

    def render(self, screen, camera):
        explosion_group.draw(screen)
        explosion_group.update()
        
        pygame.draw.line(screen, self.color, (
            self.player_pos.x - camera.target.x + camera.offset.x + 15, 
            self.player_pos.y - camera.target.y + camera.offset.y + 20
        ), self.tip , 7)


class Bullet:
    def __init__(self, x = 0, y = 0, angle = 90, life = 60, speed = 25, color = "red", size = 5):
        self.position = pygame.Vector2(x + 15, y + 20)
        self.angle = angle
        self.life = life
        self.speed = speed
        self.color = color
        self.size = size
    
    def move(self):
        self.position.x += self.speed * math.sin(self.angle)
        self.position.y += self.speed * math.cos(self.angle)
        self.life -= 1
    
    def render(self, screen, camera):
        pygame.draw.circle(screen, self.color, (
            self.position.x - camera.target.x + camera.offset.x,
            self.position.y - camera.target.y + camera.offset.y)
        , self.size)


