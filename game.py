import pygame
import sys
from Player import Player
from Camera import Camera
from Block import Platform



class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        self.platforms = [Platform(0, 100, 100, 50), Platform(300, 100, 100, 50), Platform(-200, 100, 200, 50), Platform(-200, -50, 50, 50), Platform(-400, 100, 200, 50), Platform(-300, 50, 50, 50), Platform(-400, 5, 50, 50)]
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

            # platform = pygame.Rect(0 - self.camera.target.x + self.camera.offset.x, height - 100 - self.camera.target.y + self.camera.offset.y, width, height)
            pygame.draw.rect(screen, (0, 200, 20), pygame.Rect(self.player.position.x - self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y, self.player.size.x, self.player.size.y))
            pygame.draw.rect(screen, (255, 7, 156), pygame.Rect(self.player.position.x- self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y + self.player.size.y, self.player.size.x, 1))
            for platform in self.platforms:
                platform.render(self.camera, screen)

            fps.tick(60)
            pygame.display.update()
