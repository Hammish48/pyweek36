import pygame
import math

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(1120/2, 580/2)
        self.velocity = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 50)
        self.onFloor = False
    def physicsProcess(self, platforms):
        self.velocity.x = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.velocity.x -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.velocity.x += 5
            
        if not self.onFloor:
            self.velocity.y += 0.5 
        elif pygame.key.get_pressed()[pygame.K_UP]:
            self.onFloor = False
            self.velocity.y = -15

        if self.onFloor:
            self.onFloor = False
            for platform in platforms:
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
                

        # physics engine :DDDDDDD
        # the voices are getting louder
        for platform in platforms:
            # if player on next tick is in collision with platform
            if pygame.Rect(self.position.x + self.velocity.x, self.position.y + self.velocity.y, self.size.x, self.size.y).colliderect(platform.hitbox):
                print("Collision")
                if self.position.x + self.size.x > platform.position.x and self.position.x < platform.position.x + platform.size.x:
                    # collision with top or bottom of player
                    self.velocity.y = 0
                    if self.position.y < platform.position.y:
                        self.position.y = platform.position.y - self.size.y
                        self.onFloor = True
                    elif self.position.y > platform.position.y + platform.size.y - 3:
                        self.position.y = platform.position.y + platform.size.y

                if self.position.y + self.size.y > platform.position.y and self.position.y < platform.position.y + platform.size.y:
                    # collision with side of player
                    self.velocity.x = 0
                    if self.position.x < platform.position.x:
                        self.position.x = platform.position.x - self.size.x
                    else:
                        self.position.x = platform.position.x + platform.size.x

        self.position += self.velocity

    def render(self, screen):
            # bit of pythag
            point1 = (self.player.position.x - self.camera.target.x + self.camera.offset.x + self.player.size.x, 
                self.player.position.y - self.camera.target.y + self.camera.offset.y + self.player.size.y/2-10 )

            point2 = pygame.mouse.get_pos()

            # Calculate the distance between the two points
            dx = point2[0] - point1[0]
            dy = point2[1] - point1[1]

            # Calculate the length of the line
            line_length = math.sqrt(dx**2 + dy**2)

            # only 10
            if line_length > 20:
                scale_factor = 20 / line_length
                dx *= scale_factor
                dy *= scale_factor

            
            new_point2 = (point1[0] + dx, point1[1] + dy)


            
            pygame.draw.rect(screen, (0, 200, 20), pygame.Rect(self.player.position.x - self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y, self.player.size.x, self.player.size.y))
            pygame.draw.rect(screen, (255, 7, 156), pygame.Rect(self.player.position.x- self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y + self.player.size.y, self.player.size.x, 1))
            pygame.draw.line(screen, "red", point1 ,new_point2, 5)
