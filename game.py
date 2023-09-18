import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform
from Enemies import *


class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        # self.platforms = [Platform(0, 100, 100, 50), Platform(300, 100, 100, 50), Platform(-200, 100, 200, 50), Platform(-200, -50, 50, 50), Platform(-400, 100, 200, 50), Platform(-300, 50, 50, 50), Platform(-400, 5, 50, 50)]
        self.platforms = []
        self.flyingEnemies = [FlyingEnemy(200, 200, 1)]
        # self.map = []

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
                    self.platforms.append(Platform(x, y, 50, 50, 2))  # Adjust x, y, width, and height as needed
                    print(x, y, 50, 50)
                if char == '2':
                    self.platforms.append(Platform(x, y, 50, 50, 1))
                    print(x, y, 50, 50)
                if char == '3':
                    self.platforms.append(Platform(x, y, 50, 50, 3))
                x += 50  # Increment x position based on platform width
            y += 50  # Increment y position based on platform height
        
    
    def run(self,screen, fps):        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # game logic
            self.player.physicsProcess(self.platforms)
            for enemy in self.flyingEnemies:
                enemy.fly(self.platforms)
            # rendering
            screen.fill((255, 255, 255))

            self.player.renderscreen, self.platforms, self.camera)


            for platform in self.platforms:
                platform.render(self.camera, screen)
            for enemy in self.flyingEnemies:
                pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(enemy.position.x - self.camera.target.x + self.camera.offset.x, enemy.position.y- self.camera.target.y + self.camera.offset.y, 50, 30))

            fps.tick(60)
            pygame.display.update()
