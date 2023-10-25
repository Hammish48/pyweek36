import pygame
import sys
import math
from UI import drawText, Button
import game
class Startup:
    def __init__(self) -> None:
        self.startup = True
        self.card = 0
        self.cards = 4

    def run(self,screen, fps):        
        next = Button(0, 0, 100, 100)
        while self.startup:
            screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.card < self.cards and self.card > 0:
                    self.card += 1


            match self.card:
                case 0:
                    screen.blit(pygame.image.load("assets/main.png").convert(), (0, 0))
                    if Button(45, 270, 180, 700).onClick():
                        self.card += 1
                    if Button(160, 380, 180, 700).onClick():
                        pygame.quit()
                        sys.exit()
                case 1:
                    screen.blit(pygame.image.load("assets/startup_1.png").convert(), (0, 0))
                case 2:
                    screen.blit(pygame.image.load("assets/startup_2.png").convert(), (0, 0))
                case 3:
                    break
       
            fps.tick(60)
            pygame.display.update()
        g = game.Game()
        g.load_map("level_1")
        g.run(screen, fps)
