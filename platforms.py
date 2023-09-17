import pygame

class Platform:
    def __init__(self, x, y, width, height, camera, screen):
        self.rect = pygame.Rect(x - camera.target.x + camera.offset.x, y - camera.target.y + camera.offset.y, width, height)
        pygame.draw.rect(screen, (0,0,0), self.rect)
