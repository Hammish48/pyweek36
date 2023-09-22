import pygame
import sys
import math
from UI import drawText, Button

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
                if event.type == pygame.MOUSEBUTTONDOWN and self.card < self.cards:
                    self.card += 1


            match self.card:
                case 0:
                    drawText(screen, "main menu", 100, 100)
                case 1:
                    screen.blit(pygame.image.load("assets/startup_1.png"), (0, 0))
                case 2:
                    drawText(screen, "cut scene no 2", 100, 100)
                case 3:
                    self.startup = False
       
            fps.tick(60)
            pygame.display.update()
