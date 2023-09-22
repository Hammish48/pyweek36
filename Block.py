import pygame

class Platform:
    textures = {
        "dirt block":pygame.image.load("assets/" + "dirt block" + ".png").convert_alpha(),
        "grass block":pygame.image.load("assets/" + "grass block" + ".png").convert_alpha(),
        "stone block":pygame.image.load("assets/" + "stone block" + ".png").convert_alpha(),
        "brick block":pygame.image.load("assets/" + "brick block" + ".png").convert_alpha()
    }
    darktextures = {
        "dark block":pygame.image.load("assets/" + "dirt block" + ".png").convert_alpha(),
        "dark stone block":pygame.image.load("assets/" + "dark stone block" + ".png").convert_alpha(),
        "dark brick block":pygame.image.load("assets/" + "dark brick block" + ".png").convert_alpha()
    }
    def __init__(self, x, y, width, height, texture, darktexture="dark block"):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.texture = self.textures[texture]
        self.darktexture = self.darktextures[darktexture]
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
