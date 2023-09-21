import pygame
import sys
import math


class Button:
    def __init__(self, x, y, width, height) -> None:
        self.position = pygame.Vector2(x, y)
        self.height = height
        self.width = width
    def onClick(self):
        if not pygame.Rect(self.position.x, self.position.y, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
            return False
        if pygame.mouse.get_pressed()[0]:
            return True
        return False
    def show(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.position.x, self.position.y, self.width, self.height))

def drawText(screen, text = "Hello, World.", x = 0, y = 0, size = 10, font="Helvetica-Bold.ttf", color=(0,0,0)):
    screen.blit(pygame.font.Font(f"./assets/{font}").render(text, True, color), (x, y))



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
