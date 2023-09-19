import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform
from Enemies import *
from Cure import Cure
import math


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

    def load_map(self, path):
        with open(path + ".txt", "r") as f:
            data = f.read().split("\n")

        y = 0
        for row in data:
            x = 0
            for char in row:
                match char:
                    case '1':
                        self.platforms.append(Platform(x, y, 50, 50, "dirt block"))
                    case '2':
                        self.platforms.append(Platform(x, y, 50, 50, "grass block"))
                    case '3':
                        self.platforms.append(Platform(x, y, 50, 50, "brick block"))
                    case '4':
                        self.platforms.append(Platform(x, y, 50, 50, "stone block"))
                    case '5':
                        self.groundEnemies.append(GroundEnemy(x, y))
                    case '6':
                        self.flyingEnemies.append(FlyingEnemy(x, y, 1))
                    case 'c':
                        self.cures.append(Cure(x, y))
                    case 'i':
                        self.cures.append(Platform(x, y, 50, 50, "dark block"))
                x += 50  # Increment x position based on platform width
            y += 50  # Increment y position based on platform height
        
    
    def run(self,screen, fps, main):        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if not self.player.alive and pygame.mouse.get_pressed()[0]:  
                game = Game()
                game.load_map("level_1")
                game.run()


            # game logic
            if self.player.alive:
                if self.player.health < 0:
                    self.player.alive = False
                self.player.physicsProcess(self.platforms, self.groundEnemies, self.camera, self.flyingEnemies, self.cures)
                for enemy in self.flyingEnemies:
                    enemy.fly(self.platforms, self.player)
                    for index, projectile in enumerate(enemy.projectiles):
                        if pygame.Rect(projectile.position.x, projectile.position.y, 20, 20).colliderect(self.player.hitbox):
                            self.player.health -= 20
                            enemy.projectiles.pop(index)
                        for platform in self.platforms:
                            if pygame.Rect(projectile.position.x, projectile.position.y, 20, 20).colliderect(platform.hitbox) and len(enemy.projectiles):
                                enemy.projectiles.pop(index)
                                break
                for enemy in self.groundEnemies:
                    enemy.move(self.platforms)

                # rendering
                screen.fill((52, 192, 255))

                for x in range(-2, 5):
                    for y in range(-2, 5):
                        screen.blit(self.bg, (
                            self.player.position.x/3  - self.camera.target.x + self.camera.offset.x + (x*1120),
                            self.player.position.y/3 - self.camera.target.y + self.camera.offset.y + (y*580))
                        )
                
                self.player.render(screen, self.platforms, self.camera, self.groundEnemies)
    
                for platform in self.platforms:
                    if math.hypot(platform.position.y - self.player.position.y, platform.position.x - self.player.position.x) > 750:
                        continue
                    platform.render(self.camera, screen)
                for enemy in self.flyingEnemies:
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 800:
                        continue
                    screen.blit(enemy.sprite, (enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y))
                    #pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y, 50, 30))
                    for projectile in enemy.projectiles:
                        pygame.draw.rect(screen, (255, 255, 50), pygame.Rect(projectile.position.x - self.camera.target.x + self.camera.offset.x, projectile.position.y- self.camera.target.y + self.camera.offset.y, 20, 20))
                for enemy in self.groundEnemies:
                    if math.hypot(enemy.position.y - self.player.position.y, enemy.position.x - self.player.position.x) > 800:
                        continue
                    enemy.render(screen, self.camera)
                    if enemy.hitbox.colliderect(self.player.hitbox):
                        self.player.health -= 3
                for cure in self.cures:
                    cure.render(self.camera, screen)
                
                
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, 10 ,(self.player.health/100)*580))
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, (self.player.infection/100)*1120, 10))

                # places screen that slowly increses opacity - tied to infection
                s = pygame.Surface((1120,580)) 
                s.set_alpha((self.player.infection/100) * 255)     # alpha level
                s.fill((0,random.randint(0, 5),random.randint(0, 5))) # epelepsy if too random?    
                screen.blit(s, (0,0))
            else:
                screen.blit(self.death, (0, 0))

            fps.tick(60)
            pygame.display.update()
