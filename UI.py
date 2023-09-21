import pygame
import sys
class Button:
    def __init__(self, x, y, width, height) -> None:
        self.position = pygame.Vector2(x, y)
        self.height = height
        self.width = width
    def onClick(self):
        if not pygame.Rect(self.position.x, self.position.y, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
            return False
        if pygame.mouse.get_pressed()[0]:
            return True
        return False
    def show(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.position.x, self.position.y, self.width, self.height))
        




class DeathScreen:
    def __init__(self) -> None:
        pass
    def show(self, screen, fps, game):
        restart = Button(200, 425, 220, 100)
        quit = Button(450, 425, 220, 100)
        screen.blit(pygame.image.load("./assets/death.png"), (0,0))
        pygame.display.update()
        while (1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if quit.onClick():
                sys.exit()
            if restart.onClick():
                g = game()
                g.load_map("level_1")
                g.run(screen, fps)
            fps.tick(30)


