import pygame

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(100, 100)
        self.velocity = pygame.Vector2(0, 5)
        self.size = pygame.Vector2(50, 50)
    def physicsProcess(self):
        self.position += self.velocity