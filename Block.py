import pygame

# assets\top_block.png

class Platform:
    def __init__(self, x, y, width, height, texture):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.texture = texture
    def render(self, camera, screen):
        self.rect = pygame.Rect(self.position.x - camera.target.x + camera.offset.x, self.position.y - camera.target.y + camera.offset.y, self.size.x, self.size.y)
        if self.texture == 1:
            screen.blit(pygame.image.load("assets/grass block.png"), (self.position.x- camera.target.x + camera.offset.x, self.position.y- camera.target.y + camera.offset.y))
        elif self.texture == 2:
            screen.blit(pygame.image.load("assets/dirt block.png"), (self.position.x- camera.target.x + camera.offset.x, self.position.y- camera.target.y + camera.offset.y))
        elif self.texture == 3:
            pygame.draw.rect(screen, "red", self.rect)
