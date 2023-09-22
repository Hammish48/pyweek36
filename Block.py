import pygame

class Platform:
    def __init__(self, x, y, width, height, texture, darktexture="dark block"):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.texture = pygame.image.load("assets/" + texture + ".png").convert_alpha()
        self.darktexture = pygame.image.load("assets/" + darktexture + ".png").convert_alpha()
        self.dark = False
    def render(self, camera, screen):
        #self.rect = pygame.Rect(
        #    self.position.x - camera.target.x + camera.offset.x,
        #    self.position.y - camera.target.y + camera.offset.y,
        #    self.size.x,
        #    self.size.y
        #)
        #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
        #    self.position.x - camera.target.x + camera.offset.x + 4,
        #    self.position.y - camera.target.y + camera.offset.y + 4,
        #    self.size.x,
        #    self.size.y
        #))
        if not self.dark:
            screen.blit(self.texture, self.position - camera.target + camera.offset)
        else:
            screen.blit(self.darktexture, self.position - camera.target + camera.offset)
