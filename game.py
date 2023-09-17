import pygame
import sys
from Player import Player
from Camera import Camera

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))

    def run(self,screen, fps):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # game logic
            self.player.physicsProcess()
            # rendering
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(200- self.camera.target.x + self.camera.offset.x, 100 - self.camera.target.y + self.camera.offset.y, 100, 50))
            pygame.draw.rect(screen, (0, 200, 20), pygame.Rect(self.player.position.x - self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y, 50,50))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(1120/2, 580/2, 2, 2))

            fps.tick(60)
            pygame.display.update()