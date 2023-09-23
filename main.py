import pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((1120, 580))
    pygame.display.set_caption('A dying world - pyweek 36')
    pygame.display.set_icon(pygame.image.load("./assets/dark brick block.png"))
    fps = pygame.time.Clock()
    from startup import Startup
    startup = Startup()

    startup.run(screen, fps)

    

if __name__ == "__main__":
    main()
