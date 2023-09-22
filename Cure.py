import pygame

class Cure:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(50, 50)
        self.hitbox = pygame.Rect(x, y, 50, 50)
        self.sprite = pygame.image.load("assets/cure.png").convert_alpha()
    def render(self, camera, screen):
        
        screen.blit(self.sprite, self.position - camera.target + camera.offset)

