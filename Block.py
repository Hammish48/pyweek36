import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
    def render(self, camera, screen):
        self.rect = pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, self.size.x, self.size.y)
        pygame.draw.rect(screen, (0,0,0), self.rect)
