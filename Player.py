import pygame
import math

class Player():
    def __init__(self) -> None:
        self.position = pygame.Vector2(1120/2, 580/2)
        self.velocity = pygame.Vector2(0, 1)
        self.size = pygame.Vector2(30, 50)
        self.onFloor = False
        self.forward = True
        self.sprite = pygame.image.load("assets/player/walk 5.png")
        self.bullets = []
        self.shoot_cooldown = 0  # Initialize the cooldown timer to 0
        self.shoot_cooldown_duration = 30
    def physicsProcess(self, platforms):
        self.velocity.x = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.velocity.x -= 5
            if self.forward:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                print("fliped")
            self.forward = False
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.velocity.x += 5
            if not self.forward:
                self.sprite =pygame.transform.flip(self.sprite, True, False)
                print("fliped")
            self.forward = True
            
        if not self.onFloor:
            self.velocity.y += 0.5 
        elif pygame.key.get_pressed()[pygame.K_w]:
            self.onFloor = False
            self.velocity.y = -15

        if self.onFloor:
            self.onFloor = False
            for platform in platforms:
                if platform.hitbox.colliderect(pygame.Rect(self.position.x, self.position.y + self.size.y + 1, self.size.x, 1)):
                    self.onFloor = True
                

        # physics engine :DDDDDDD :)
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

    def render(self, screen, platforms):
        player = pygame.image.load("assets\\player.png").convert_alpha()
        # pygame.draw.rect(screen, (0, 200, 20), pygame.Rect(self.player.position.x - self.camera.target.x + self.camera.offset.x, self.player.position.y - self.camera.target.y + self.camera.offset.y, self.player.size.x, self.player.size.y))
        screen.blit(self.sprite, self.position - camera.target + camera.offset)

        # get pos of hand on player
        hand_pos = pygame.math.Vector2(
            self.player.position.x - self.camera.target.x + self.camera.offset.x + self.player.size.x - self.player.size.x/2, 
            self.player.position.y - self.camera.target.y + self.camera.offset.y + self.player.size.y-30
        )

        # get cursor pos
        cursor = pygame.math.Vector2(pygame.mouse.get_pos())
        direction = cursor - hand_pos

        if direction.x != 0 or direction.y != 0:
            direction.normalize_ip()
        
        end = hand_pos + direction * 30

        
        angle = math.atan2(direction.x, direction.y)


    


        if pygame.mouse.get_pressed()[0] and self.player.shoot_cooldown == 0:
            # Check if the left mouse button is pressed and cooldown is zero
            self.player.bullets.append([angle, self.player.position.x, self.player.position.y, 60])
            print(self.player.bullets)

            # Set the cooldown timer to the cooldown duration
            self.player.shoot_cooldown = self.player.shoot_cooldown_duration

        if self.player.shoot_cooldown > 0:
            self.player.shoot_cooldown -= 1  # Decrement the cooldown timer



        bullets_to_remove_indices = []  # Create a list to store the indices of bullets to be removed

        for index, bullet in enumerate(self.player.bullets):
            pygame.draw.circle(screen, "black", (
                bullet[1] - self.camera.target.x + self.camera.offset.x + self.player.size.x - self.player.size.x / 2,
                bullet[2] - self.camera.target.y + self.camera.offset.y + self.player.size.y - 30), 5)
            
            bullet[1] = bullet[1] + 25 * math.sin(bullet[0])
            bullet[2] = bullet[2] + 25 * math.cos(bullet[0])
            bullet[3] -= 1

            if bullet[3] == 0:
                # Mark this bullet for removal by storing its index
                bullets_to_remove_indices.append(index)
            for platform in platforms:
                if platform.hitbox.collidepoint((bullet[1], bullet[2])):
                    bullets_to_remove_indices.append(index)

        # Remove the marked bullets in reverse order to avoid index issues
        for index in reversed(bullets_to_remove_indices):
            del self.player.bullets[index]


        pygame.draw.line(screen, "black", hand_pos, end, 14)
