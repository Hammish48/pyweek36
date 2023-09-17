import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
    def render(self,camera, screen):
        self.rect = pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, 1120, 580)
        pygame.draw.rect(screen, (0,0,0), self.rect)
        
