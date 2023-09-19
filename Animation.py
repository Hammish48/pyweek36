import pygame


class AnimationPlayer:
    def __init__(self, frames:list) -> None:
        self.frames = frames
        self.time = frames[0].time
        self.currentframe = 0
        self.maxframes = len(self.frames) -1
    def tick(self):
        self.time -= 1
        if self.time <= 0:
            if self.currentframe < self.maxframes:
                self.currentframe += 1
            else:
                self.currentframe = 0
            self.time = self.frames[self.currentframe].time
    def getCurrentFrame(self):
        return self.frames[self.currentframe].img


class AnimationFrame:
    def __init__(self, img:pygame.Surface, time:int) -> None:
        self.time = time
        self.img = img