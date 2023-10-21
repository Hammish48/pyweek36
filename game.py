import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform
from Enemies import *
from Cure import Cure
import math
import UI
from Healthboost import HealthBoost

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        self.platforms = []
        self.flyingEnemies = []
        self.groundEnemies = []
        self.cures = []
        self.death = pygame.image.load("assets/death.png")
        self.bg = pygame.image.load("assets/background.png")
        self.healthboosts = []
        self.dark = 0
        self.Won = False
        self.winfadetime = 0
    def load_map(self, path):
        with open(path + ".txt", "r") as f:
            data = f.read().split("\n")

        y = -550
        for row in data:
            x = -3450
            for char in row:
                match char:
                    case '1':
                        self.platforms.append(Platform(x, y, 50, 50, "dirt block"))
                    case '2':
                        self.platforms.append(Platform(x, y, 50, 50, "grass block"))
                    case '3':
                        self.platforms.append(Platform(x, y, 50, 50, "brick block", "dark brick block"))
                    case '4':
                        self.platforms.append(Platform(x, y, 50, 50, "stone block", "dark stone block"))
                    case '5':
                        self.groundEnemies.append(GroundEnemy(x, y))
                    case '6':
                        self.flyingEnemies.append(FlyingEnemy(x, y, 1))
                    case 'c':
                        self.cures.append(Cure(x, y))
                    case 'i':
                        self.cures.append(Platform(x, y, 50, 50, "dark block"))
                    case 'h':
                        self.healthboosts.append(HealthBoost(x, y))
                x += 50  # Increment x position based on platform width
            y += 50  # Increment y position based on platform height
        
    
    def run(self,screen, fps):        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # game logic
            if self.player.alive:
                if self.player.health < 0:
                    self.player.alive = False
                if not self.Won : self.player.physicsProcess(self.platforms, self.groundEnemies, self.camera, self.flyingEnemies, self.cures, self.healthboosts)
                for enemy in self.flyingEnemies:
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 1100:
                        continue
                    enemy.fly(self.platforms, self.player)
                    for index, projectile in enumerate(enemy.projectiles):
                        if pygame.Rect(projectile.position.x, projectile.position.y, 20, 20).colliderect(self.player.hitbox):
                            self.player.health -= 20
                            self.player.infection += 8
                            enemy.projectiles.pop(index)
                        for platform in self.platforms:
                            if pygame.Rect(projectile.position.x, projectile.position.y, 20, 20).colliderect(platform.hitbox) and len(enemy.projectiles):
                                enemy.projectiles.pop(index)
                                break
                for enemy in self.groundEnemies:
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 900:
                        continue

                    enemy.move(self.platforms)
                self.dark = 0
                for platform in self.platforms:
                    if platform.dark:
                        self.dark += 1
                if self.dark == 0 and len(self.groundEnemies) + len(self.flyingEnemies) == 0:
                    self.Won = True
                    self.player.health = 100
                    self.player.infection = 0
                # rendering
                if not self.Won:
                    for x in range(-5, 5):
                        if self.player.position.x/3 + (x*1120) - self.player.position.x > 1000 or self.player.position.x/3 + (x*1120) - self.player.position.x < -1800:
                            continue
                        for y in range(-5, 5):
                            if self.player.position.y/3 + y*580 - self.player.position.y > 600 or self.player.position.y/3 + y*580 - self.player.position.y  < -1000:
                                continue
                            screen.blit(self.bg, (
                                self.player.position.x/3  - self.camera.target.x + self.camera.offset.x + (x*1120),
                                self.player.position.y/3 - self.camera.target.y + self.camera.offset.y + (y*580))
                            )
                else:
                    screen.fill((22, 183, 255))
    
                for platform in self.platforms:
                    if math.hypot(platform.position.y - self.player.position.y, platform.position.x - self.player.position.x) > 670:
                        continue
                    platform.render(self.camera, screen)
                for enemy in self.flyingEnemies:
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 700:
                        continue
                    enemy.animation.tick()
                    if enemy.direction > 0:
                        screen.blit(pygame.transform.flip(enemy.animation.getCurrentFrame(), True, False), (enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y))
                    else:
                        screen.blit(enemy.animation.getCurrentFrame(), (enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y))
                    for projectile in enemy.projectiles:
                        pygame.draw.rect(screen, (255, 255, 50), pygame.Rect(projectile.position.x - self.camera.target.x + self.camera.offset.x, projectile.position.y- self.camera.target.y + self.camera.offset.y, 20, 20))
                for index, enemy in enumerate(self.groundEnemies):
                    if enemy.velocity.y > 15:
                        self.groundEnemies.pop(index)
                        continue
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 700:
                        continue
                    enemy.render(screen, self.camera)
                    if enemy.hitbox.colliderect(self.player.hitbox):
                        self.player.health -= .5
                        self.player.infection += .5
                for cure in self.cures:
                    cure.render(self.camera, screen)
                for healthboost in self.healthboosts:
                    healthboost.render(screen, self.camera)

                self.player.render(screen, self.platforms, self.camera, self.groundEnemies)

                # places screen that slowly increses opacity - tied to infection
                if self.player.infection > 60:
                    s = pygame.Surface((1120,580)) 
                    s.set_alpha((self.player.infection/160) * 165 + 90)     # alpha level
                    s.fill((0,random.randint(0, 5),random.randint(0, 5))) # epelepsy if too random?    
                    screen.blit(s, (0,0))
                UI.GameUI.show(screen, self.player, self, fps) 
                if self.Won:
                    s = pygame.Surface((1120, 580))
                    s.set_alpha(self.winfadetime)
                    s.blit(UI.endscreen, (0,0))
                    screen.blit(s, (0,0))
                    self.winfadetime+=1
                    if self.winfadetime > 200:
                        UI.Winscreen.show(screen, fps)
                
            else:
                death = UI.DeathScreen()
                death.show(screen, fps, Game)

            fps.tick(60)
            pygame.display.update()

