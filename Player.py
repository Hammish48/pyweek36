import pygame

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(10, -100)
        self.velocity = pygame.Vector2(0, 5)
        self.acceleration = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 30)
    def physicsProcess(self):
        self.velocity.x = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.velocity.x -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.velocity.x += 5
        
        self.position += self.velocity
        self.velocity += self.acceleration
