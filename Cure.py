import pygame

class Cure:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(50, 50)
        self.hitbox = pygame.Rect(x, y, 50, 50)
    def render(self, camera, screen):
        self.rect = pygame.Rect(
            self.position.x - camera.target.x + camera.offset.x,
            self.position.y - camera.target.y + camera.offset.y,
            self.size.x,
            self.size.y
        )
        
        screen.blit(pygame.image.load("assets/cure.png").convert_alpha(), self.rect)
