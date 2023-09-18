import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform


class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        # self.platforms = [Platform(0, 100, 100, 50), Platform(300, 100, 100, 50), Platform(-200, 100, 200, 50), Platform(-200, -50, 50, 50), Platform(-400, 100, 200, 50), Platform(-300, 50, 50, 50), Platform(-400, 5, 50, 50)]
        self.platforms = []
        self.enemies = []
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
                    self.platforms.append(Platform(x, y, 50, 50, "brown"))  # Adjust x, y, width, and height as needed
                    print(x, y, 50, 50)
                if char == '2':
                    self.platforms.append(Platform(x, y, 50, 50, "green"))  # Adjust x, y, width, and height as needed
                    print(x, y, 50, 50)
                if char == '3':
                    self.platforms.append(Platform(x, y, 50, 50, "red"))
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
            # rendering
            screen.fill((255, 255, 255))

            Player.render(self, screen)


            for platform in self.platforms:
                platform.render(self.camera, screen)

            fps.tick(60)
            pygame.display.update()
