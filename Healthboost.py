import pygame

class HealthBoost:
    def __init__(self, x, y) -> None:
        self.position = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(x, y, 50, 50)
        self.sprite = pygame.image.load("./assets/heart thing.png").convert_alpha()
    def render(self, screen, camera):
        screen.blit(self.sprite, self.position - camera.target + camera.offset)
