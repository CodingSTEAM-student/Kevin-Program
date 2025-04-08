import pygame
import os


class Object_ani:

    def __init__(self, image:str, name:str, frames:int, row:int,
            base_width:int, base_height:int, base_offsetw:int, base_offseth:int,
            frame_width:int, frame_height:int, frame_offsetw:int, frame_offseth:int,
            animationdelay:int, scale=2):
        self.name = name
        self.images = []
        self.animation_delay = animationdelay
        self.pause = 0
        self.index = 0
        self.end_subscribers = []
    
        for num in range(frames):
            object = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            # if DEBUGGER: object.fill("red")
    
            object.blit(image, (frame_offsetw, frame_offseth),
                        (num * base_width + base_offsetw, base_height * row +
                         base_offseth, base_width, base_height))
            object = pygame.transform.scale_by(object, scale)
            self.images.append(object)
        self.image = self.images[int(0)]
        self.length = len(self.images)
    
    def set_pause_time(self, time):
        self.pause = time
        self.stop = time
    
    def run(self):
        if self.index == 0 and self.pause > 0:
            if self.stop != 0:
                self.stop -= 1
                return
            self.stop = self.pause
        self.index += self.animation_delay
    
        if self.index >= self.length:
            self.index = 0
            for subscriber in self.end_subscribers:
                subscriber()
        self.image = self.images[int(self.index)]
    
    def __repr__(self):
        return "{} {}".format(self.name, self.images)
    
    def export(self):
        try:
            os.mkdir("export")
        except FileExistsError:
            pass
        for i, image in enumerate(self.images):
            pygame.image.save(image, "export/{}{}.png".format(self.name, i))
    
        