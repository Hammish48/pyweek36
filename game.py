import pygame
import sys
from Player import Player
from Camera import Camera
from platforms import Platform






class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.camera = Camera(self.player.position, pygame.Vector2(560 - self.player.size.x/2, 290 - self.player.size.y/2))
        self.platforms = [Platform(100, 100, 100, 50)]
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
            # platform = pygame.Rect(0 - self.camera.target.x + self.camera.offset.x, height - 100 - self.camera.target.y + self.camera.offset.y, width, height)

            pygame.draw.rect(screen, (0, 200, 20), player)

            p_1 = Platform(0, height-100, width, 100, self.camera, screen)
            # pygame.draw.rect(screen, (0,0,0), p_1.rect)


            
            if player.colliderect(p_1.rect):
                print("collide")
                self.player.velocity = pygame.Vector2(0, 0)
                self.player.acceleration = pygame.Vector2(0, 0)
                self.player.position -= pygame.Vector2(0, 1)
            


            fps.tick(60)
            pygame.display.update()
