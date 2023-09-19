import pygame
import sys
from game import Game

pygame.init()

def main():
    screen = pygame.display.set_mode((1120, 580))
    pygame.display.set_caption("caption")
    fps = pygame.time.Clock()
    game = Game()

    game.load_map("level_1")
    game.run(screen, fps, main)
    

if __name__ == "__main__":
    main()
