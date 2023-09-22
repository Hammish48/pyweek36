import pygame
import sys
from startup import Startup

pygame.init()

def main():
    screen = pygame.display.set_mode((1120, 580))
    pygame.display.set_caption('I love the part where he said "its gaming time" and then gamed everywhere')
    fps = pygame.time.Clock()
    from game import Game
    game = Game()
    startup = Startup()

    startup.run(screen, fps)

    game.load_map("level_1")
    game.run(screen, fps)
    

if __name__ == "__main__":
    main()
