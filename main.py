import pygame
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
def main():
    pygame.mixer.music.load("assets/Space Fighter Loop.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((1120, 580))
    pygame.display.set_caption('A dying world - pyweek 36')
    pygame.display.set_icon(pygame.image.load("./assets/dark block.png").convert())
    fps = pygame.time.Clock()
    from startup import Startup
    startup = Startup()

    startup.run(screen, fps)

    

main()
