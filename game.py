import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform
from Enemies import *
import math


class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        self.platforms = []
        self.flyingEnemies = [FlyingEnemy(200, 50, 1)]
        self.groundEnemies = [GroundEnemy(180, -50)]
        # self.map = []
        self.death = pygame.image.load("assets/death.png")

    def load_map(self, path):
        x = 0
        y = 0
        f = open(path + ".txt", "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            x = 0
            for char in row:
                if char == '1':
                    self.platforms.append(Platform(x, y, 50, 50, "dirt block"))  # Adjust x, y, width, and height as needed
                if char == '2':
                    self.platforms.append(Platform(x, y, 50, 50, "grass block"))
                if char == '3':
                    self.platforms.append(Platform(x, y, 50, 50, "brick block"))
                if char == '4':
                    self.platforms.append(Platform(x, y, 50, 50, "stone block"))
                if char == '5':
                    self.groundEnemies.append(GroundEnemy(x, y))
                if char == '6':
                    self.flyingEnemies.append(FlyingEnemy(x, y, 1))
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
                game.run(screen, fps, main)                    
                print("aaaa")
            # game logic
            if self.player.alive:
                if self.player.health < 0:
                    self .player.alive = False
                self.player.physicsProcess(self.platforms, self.groundEnemies, self.camera)
                for enemy in self.flyingEnemies:
                    enemy.fly(self.platforms, self.player)
                    for index, projectile in enumerate(enemy.projectiles):
                        if pygame.Rect(projectile.position.x, projectile.position.y, 20, 20).colliderect(self.player.hitbox):
                            self.player.health -= 20
                            enemy.projectiles.pop(index)
                for enemy in self.groundEnemies:
                    enemy.move(self.platforms)
                # rendering
                screen.fill((52, 192, 255))
    
                self.player.render(screen, self.platforms, self.camera, self.groundEnemies)
    
    
                for platform in self.platforms:
                    platform.render(self.camera, screen)
                for enemy in self.flyingEnemies:
                    pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y, 50, 30))
                    for projectile in enemy.projectiles:
                        pygame.draw.rect(screen, (255, 255, 50), pygame.Rect(projectile.position.x - self.camera.target.x + self.camera.offset.x, projectile.position.y- self.camera.target.y + self.camera.offset.y, 20, 20))
                for enemy in self.groundEnemies:
                    enemy.render(screen, self.camera)
                    if enemy.hitbox.colliderect(self.player.hitbox):
                        self.player.health -= 3
                
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, (self.player.health/100)*1120, 10))
            else:
                screen.blit(self.death, (0, 0))

            fps.tick(60)
            pygame.display.update()
