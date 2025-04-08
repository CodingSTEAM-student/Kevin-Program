import pygame
from pygame.image import load as load_image
from animation_loading import Object_ani

class Player:
    def __init__(self, anims_info, x, y):
        self.animations = []
        self.is_jumping = False
        self.speed = 0
        self.gravity = 0
        self.x = x
        self.y = y

        self.health = 80

        for info in anims_info:
            file = "graphics/Knight_2/" + info[0].capitalize() + ".png"
            image = load_image(file)
            player_ani = Object_ani(image, *info)
            self.animations.append(player_ani)
        self.set_state("idle")
        self.last_state = None
        for animation in self.animations:
            if animation.name == "idle":
                animation.set_pause_time(120)

        self.recta = self.animation.image.get_rect(midbottom=(x, y))
        self.hitbox=self.recta.copy()
        self.hitbox.width-=30
        self.hitbox.height-=20
        self.hitbox.midbottom = self.recta.midbottom
        print(self.hitbox)
        self.hitbox_extras = {
            "attack 3": pygame.Rect(240, 325, 90, 100)
        }

    def set_state(self, state):
        self.state = state
        if DEBUGGER:
            print("Setting player state to:", state)
        for i in range(len(self.animations)):
            anim = self.animations[i]
            if anim.name == self.state:

                self.animation = self.animations[i]

    def update(self):
        self.gravity_check()
        self.move()
        self.hitbox.midbottom = self.recta.midbottom
        self.animation.run()

    def move(self, forward=True):
        if forward:
            self.x = self.x + (self.speed)
        else:
            self.x = self.x - (self.speed)
        self.recta = self.animation.image.get_rect(midbottom=(self.x, self.y))

    def gravity_check(self):
        if self.y <= 425:
            self.gravity = self.gravity + 0.3

        self.y = self.y + (self.gravity)

        if self.is_jumping == True:
            if self.y > 425:
                self.is_jumping = False
                if self.speed == 0:
                    self.set_state("idle")
                elif self.last_state != None or self.last_state != "idle":
                    self.set_state(self.last_state)


        if self.y > 425:
            self.y = 425
            self.recta.bottom = 425
            self.gravity = 0

    def walk(self):
        self.speed = -3
        if not self.is_jumping:
            self.set_state("walk")
        else:
            self.last_state = "walk"

    def run(self):
        self.speed = 4
        if not self.is_jumping:
            self.set_state("run")
        else:
            self.last_state = "run"

    def attack(self):
        self.last_state = self.state
        self.set_state("attack 3")

    def stop(self):
        self.speed = 0
        if self.is_jumping:
            self.last_state = None
        if not self.is_jumping:
            self.set_state("idle")

    def jump(self):
        if not self.is_jumping:
            self.last_state = self.state
            self.set_state("jump")
            self.gravity = -10
            self.is_jumping = True

    def draw(self):
        screen.blit(
            self.animation.image,
            self.animation.image.get_rect(midbottom=self.recta.midbottom))
        self.display_health()
        if DEBUGGER:
            pygame.draw.rect(screen, "black", self.recta, 4)
            pygame.draw.circle(screen, "red", self.recta.bottomleft, 5)
            pygame.draw.circle(screen, "blue", self.recta.midbottom, 5)
            pygame.draw.rect(screen, "orange", self.hitbox, 2)
            pygame.draw.rect(screen, "red", self.hitbox_extras["attack 3"], 2)

    def display_health(self):
        scale = 3
        main_bar = pygame.Rect((10, 10, 100 * scale, 10 * scale))
        pygame.draw.rect(screen, "red", main_bar)
        main_bar.width = self.health * scale
        pygame.draw.rect(screen, "green", main_bar)

        scale = 1
        floating_bar = pygame.Rect((10, 10, 100 * scale, 10 * scale))
        floating_bar.midbottom = self.recta.midtop
        pygame.draw.rect(screen, "red", floating_bar)
        floating_bar.width = self.health * scale
        pygame.draw.rect(screen, "green", floating_bar)

    def previous_state(self):
        if self.last_state != "attack 3":
            self.set_state(self.last_state)


class Enemy:

    def __init__(self, anims_info, x, y):
        self.last_state = None
        self.animations = []
        self.is_jumping = False
        self.direction = "l"
        self.speed = 0
        self.gravity = 0
        self.x = x
        self.y = y
        self.health = 100
        sp = load_image('graphics/spider.png')
        for info in anims_info:
            enemy_ani = Object_ani(sp, *info)
            self.animations.append(enemy_ani)
        for animation in self.animations:
            if animation.name == "idlel" or animation.name == "idler":
                animation.set_pause_time(120)


        self.set_state("idle")    
        self.recta = self.animation.image.get_rect(midbottom=(x, y))

    def set_state(self,state):
        self.state = state + self.direction 
        if DEBUGGER:
            print("Setting enemy state to:", state,self.direction, self.state)
        for i in range(len(self.animations)):
            anim = self.animations[i]
            if anim.name == self.state:

                self.animation = self.animations[i]

    def update(self):
        self.gravity_check()
        self.move()
        self.animation.run()

    def move(self ):
        if self.direction=="r":
            self.x = self.x + (self.speed)
        elif self.direction =="l":
            self.x = self.x - (self.speed)
        else:
            raise Exception("enemy movement error")
        self.recta = self.animation.image.get_rect(midbottom=(self.x, self.y))
    def gravity_check(self):
        if self.y <= 425:
            self.gravity = self.gravity + 0.3

        self.y = self.y + (self.gravity)

        if self.is_jumping == True:
            if self.y > 425:
                self.is_jumping = False
                if self.speed == 0:
                    self.set_state("idle")
                elif self.last_state != None or self.last_state != "idle":
                    self.set_state(self.last_state)


        if self.y > 425:
            self.y = 425
            self.gravity = 0

    def walk(self):
        self.speed = 3
        if not self.is_jumping:
            self.set_state("walk")
        else:
            self.last_state = "walk"

    def run(self):
        self.speed = 4
        if not self.is_jumping:
            self.set_state("run")
        else:
            self.last_state = "run"

    def attack(self):
        self.last_state = self.state
        self.set_state("attack 3")

    def stop(self):
        self.speed = 0
        if self.is_jumping:
            self.last_state = None
        if not self.is_jumping:
            self.set_state("idle")

    def jump(self):
        if not self.is_jumping:
            self.last_state = self.state
            self.set_state("jump")
            self.gravity = -10
            self.is_jumping = True

    def draw(self):
        screen.blit(self.animation.image, self.recta)
        self.animation.run()
        self.display_health()

        if DEBUGGER:
            pygame.draw.rect(screen, "red", self.recta, 3)
            pygame.draw.circle(screen, "red", self.recta.bottomleft, 5)
            pygame.draw.circle(screen, "blue", self.recta.midbottom, 5)

    def display_health(self):
        y_offset = 20
        scale = 1
        floating_bar = pygame.Rect((0, 0, 100 * scale, 10 * scale))
        floating_bar.midbottom = self.recta.midtop
        floating_bar.y += y_offset
        pygame.draw.rect(screen, "red", floating_bar)
        floating_bar.width = self.health * scale
        pygame.draw.rect(screen, "green", floating_bar)

    def checkscroll(self, xchange=0):
        if xchange != 0:
            self.x -= xchange
            self.recta = self.animation.image.get_rect(midbottom=(self.x,
                                                                  self.y))

