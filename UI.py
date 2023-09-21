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
        

class InfoBar:
    def __init__(self, x, y, width, height, val) -> None:
        self.position = pygame.Vector2(x, y)
        self.height = height
        self.width = width
        self.val = val
    def getRenderObject(self):
        return pygame.Rect(self.position.x, self.position.y, (self.val/100)*self.width, self.height)


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

def drawText(screen, text, x, y, size, font="Helvetica-Bold.ttf", color=(0,0,0)):
    screen.blit(pygame.font.Font(f"./assets/{font}").render(text, True, color), (x, y))

class GameUI:
    def __init__(self) -> None:
        pass
    def show(screen, player, game, clock):
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 480, 320, 100))
        drawText(screen, "heath", 0, 490, 20, color=(255, 255, 255))
        drawText(screen, "infection", 0, 510, 20, color=(255, 255, 255))
        drawText(screen, f"enemies left: {len(game.flyingEnemies) + len(game.groundEnemies)}", 0, 530, 20, color=(255, 255, 255))
        dark = 0
        for platform in game.platforms:
            if platform.dark:
                dark += 1
        drawText(screen, f"blocks left to cure: {dark}", 0, 550, 20, color=(255, 255, 255))
        drawText(screen, f"FPS: {clock.get_fps()}", 0, 570, 20, color=(255, 255, 255))
        infectionBar = InfoBar(60,510 , 230, 10, player.infection)
        healthBar = InfoBar(60, 490, 230, 10, player.health)
        pygame.draw.rect(screen, (0, 255, 0), healthBar.getRenderObject())
        pygame.draw.rect(screen, (255, 0, 0), infectionBar.getRenderObject())



