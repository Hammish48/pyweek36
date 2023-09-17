import pygame

class Camera:
    def __init__(self, target:pygame.Vector2, offset:pygame.Vector2) -> None:
        self.target = target
        self.offset = offset