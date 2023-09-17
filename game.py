import pygame
import sys
from Player import Player
from Camera import Camera
from platforms import Platform

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        self.platforms = [Platform(50, 100, 100, 50)]
    def run(self,screen, fps):
        width = 1120
        height = 580

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # game logic
            self.player.physicsProcess()
            # rendering
            screen.fill((255, 255, 255))

            player = pygame.Rect(self.player.position.x - self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y, 50,50)
            pygame.draw.rect(screen, (0, 200, 20), player)


            for platform in self.platforms:
                platform.render(self.camera, screen)
                if player.colliderect(platform.rect):
                    print("collide")
                    if abs(platform.rect.top - player.bottom) < 10:
                        self.player.velocity = pygame.Vector2(0, 0)
                        self.player.acceleration = pygame.Vector2(0, 0)
            


            fps.tick(60)
            pygame.display.update()
