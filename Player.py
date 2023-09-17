import pygame

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(10, -100)
        self.velocity = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 30)
        self.onFloor = False
    def physicsProcess(self, platforms):
        self.velocity.x = 0
        if (not self.onFloor):
            self.velocity.y += 0.5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.velocity.x -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.velocity.x += 5
        if self.onFloor and pygame.key.get_pressed()[pygame.K_UP]:
            self.onFloor = False
            self.velocity.y = -15

        if (self.onFloor):
            self.onFloor = False
            for platform in platforms:
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
                


        for platform in platforms:
            if pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y, self.size.x, self.size.y).colliderect(platform.hitbox):
                print("a")
                if self.position.x + self.size.x > platform.position.x and self.position.x < platform.position.x + platform.size.x:
                    print("b")
                    if self.position.y + 3 < platform.position.y:
                        print("c")
                        self.position.y = platform.position.y - self.size.y
                        self.velocity.y = 0
                        self.onFloor = True
                        print("d")
        print(self.onFloor)
        self.position += self.velocity
