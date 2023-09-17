import pygame
import sys

pygame.init()

def main():
    screen = pygame.display.set_mode((1120, 580))
    pygame.display.set_caption("caption")
    fps = pygame.time.Clock()
    pen = pygame.draw

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        //game logic


        //rendering
        screen.fill((0, 0, 0))

        pen.rect(screen, (0, 200, 20), pygame.Rect(50, 50, 50,50))

        fps.tick(60)
        pygame.display.update()
    

if __name__ == "__main__":
    main()
