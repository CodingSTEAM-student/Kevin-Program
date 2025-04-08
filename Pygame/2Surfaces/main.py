import ground
import pygame
from pygame.image import load as load_image
import os
import time
import random
from animation_loading import Object_ani

pygame.init()


# --------------------------------------------------------------------------------------------------------------------------
def clear():
    os.system("clear")


class Player:
    def __init__(self, anims_info, x, y):
        self.animations = []
        self.is_jumping = False
        self.speed = 0
        self.gravity = 0
        self.x = x
        self.y = y

        self.health = 80
        self.coordinates = (self.x, self.y)
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
        self.hitbox = self.recta.copy()
        self.hitbox.width -= 30
        self.hitbox.height -= 20
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
        self.hitbox_extras["attack 3"].x = self.x + 40
        self.hitbox_extras["attack 3"].y = self.y - 100
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
        self.speed = -2
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

    def attack(self, target):
        try:
            self.last_state = self.state
            self.set_state("attack 3")
            if self.state == "attack 3" and self.hitbox_extras[self.state].colliderect(target.recta):
                print("Hit enemy")
                target.get_hurt(10)

        except Exception as e:
            print("Error in player attacking: \n", e)

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

    def get_hurt(self, damage):
        self.health -= damage
        if DEBUGGER:
            print("Damaging player:", self.health)

        if self.health <= 0:
            self.death()

    def death(self):
        print("Player death")
        ...

    def previous_state(self):
        if self.last_state != "attack 3":
            self.set_state(self.last_state)

    def checkscroll(self, xchange=0):
        if xchange != 0:
            self.x -= xchange

# _________________________________________________________________


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
        self.health = 10
        self.attack_cooldown = 100
        self.attack_time = 0
        sp = load_image('graphics/spider.png')
        for info in anims_info:
            enemy_ani = Object_ani(sp, *info)
            self.animations.append(enemy_ani)
        for animation in self.animations:
            if animation.name == "idlel" or animation.name == "idler":
                animation.set_pause_time(120)

        self.set_state("idle")
        self.recta = self.animation.image.get_rect(midbottom=(x, y))

    def set_state(self, state):
        self.state = state + self.direction
        if DEBUGGER:
            print("Setting enemy state to:", state, self.direction, self.state)
        for i in range(len(self.animations)):
            anim = self.animations[i]
            if anim.name == self.state:

                self.animation = self.animations[i]

    def update(self):
        self.gravity_check()
        self.move()
        self.animation.run()
        self.checkattack()

    def move(self):
        if self.direction == "r":
            self.x = self.x + (self.speed)
        elif self.direction == "l":
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

    def checkattack(self):
        # TODO:  the attack only works once
        if self.recta.colliderect(player.recta):
            if self.attack_time == 0:
                print("attacking player")

                self.attack_time = self.attack_cooldown
                self.attack(player)
        if self.attack_time > 0:
            print("reducing attack")
            self.attack_time -= 0.1

    def attack(self, target):
        self.last_state = self.state
        try:

            print("Hit player")
            target.get_hurt(10)

        except Exception as e:
            print("Error in enemy attacking: \n", e)

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

    def get_hurt(self, damage):
        self.health -= damage
        if DEBUGGER:
            print("Damaging enemy:", self.health)

        if self.health <= 0:
            self.death()

    def death(self):
        ...


# --------------------------------------------------------------------------------------------------------------------------
screenW = 1000
screenH = 600
ground.screenW = 1000
ground.screenH = 600
running = True
DEBUGGER = True
ground.DEBUGGER = True
control_enemy = False

clickplace = False
mousepos = False
FPS = 60

deltatime = 1 / 60
previous_time = time.time()
accumulated_time = 0

player_i = [
    # name,  frames,  row,  base_width,  base_height,  base_offsetw,  base_offseth,  frame_width,  frame_height,  frame_offsetw,  frame_offseth,  animationdelay, scale:
    ("attack 3", 4, 0,  103, 76,  8,   10,  133,  76, 40,   0,  1/6.5),
    ("hurt",     2, 0,  78,  76,  0,   10,  67,   76, -5,   0,  1/7),
    ("dead",     6, 0,  76,  76,  12,  10,  84,   76, 8,    0,  1/6),
    ("idle",     4, 0,  67,  76,  0,   10,  55,   76, -15,  0,  1/7),
    ("run",      7, 0,  70,  76,  6,   10,  60,   76, -6,   0,  1/4.5),
    ("walk",     5, 0,  70,  76,  10,  10,  60,   76, -12,  0,  1/4.5),
    ("jump",     6, 0,  76,  76,  20,  10,  100,  76, 25,   0,  1/6),
]
# TODO Refactor direction out of animation name
enemy_i = [
    # name,  frames,  row,  base_width,  base_height,  base_offsetw,  base_offseth,  frame_width,  frame_height,  frame_offsetw,  frame_offseth,  animationdelay, scale:
    ["idlel",       5, 0, 32, 32, 8, 16, 16, 16, 0, 0, 1/15, 6],
    ["walkl",       6, 1, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["jumpl",       9, 2, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["webdroppingl", 1, 3, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["swingingl",   4, 4, 32, 32, 8, 16, 16, 16, 0, 0, 1/13, 6],
    ["fallingl",    3, 5, 32, 32, 8, 16, 16, 16, 0, 0, 1/25, 6],
    ["diel",        9, 6, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["webl",        6, 7, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    # right
    ["idler",       5, 8, 32, 32, 8, 16, 16, 16, 0, 0, 1/15, 6],
    ["walkr",       6, 9, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["jumpr",       9, 10, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["webdroppingr", 1, 11, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["swingingr",   4, 12, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["fallingr",    3, 13, 32, 32, 8, 16, 16, 16, 0, 0, 1/25, 6],
    ["dier",        9, 14, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
    ["webr",        6, 15, 32, 32, 8, 16, 16, 16, 0, 0, 1/10, 6],
]


screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

player = Player(player_i, 200, 425)
player.animations[5].images = list(reversed(player.animations[5].images))
player.animations[0].end_subscribers.append(player.previous_state)

enemies = []
enemies.append(Enemy(enemy_i, 400, 425))
enemies.append(Enemy(enemy_i, 600, 425))


# --------------------------------------------------------------------------------------------------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if DEBUGGER:
                player.gravity = 0

                for enemy in enemies:
                    enemy.gravity = 0

                if clickplace:
                    player.recta.topleft = event.pos
                    player.x = player.recta.x
                    player.y = player.recta.y
        if event.type == pygame.MOUSEMOTION:
            if DEBUGGER and mousepos:
                position = event.pos
                print(position)
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            right_held = pygame.key.get_pressed()[
                pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]
            left_held = pygame.key.get_pressed()[
                pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]
            right_pressed = event.key == pygame.K_d or event.key == pygame.K_RIGHT
            left_pressed = event.key == pygame.K_a or event.key == pygame.K_LEFT

            right_E_held = pygame.key.get_pressed()[
                pygame.K_l]
            left_E_held = pygame.key.get_pressed()[
                pygame.K_j]
            right_E_pressed = event.key == pygame.K_l
            left_E_pressed = event.key == pygame.K_j

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                DEBUGGER = not DEBUGGER
                ground.DEBUGGER = not ground.DEBUGGER
            if DEBUGGER:
                if event.key == pygame.K_8:
                    print("Toggeling control enemy state.")
                    control_enemy = not control_enemy

                if event.key == pygame.K_2:
                    clickplace = not clickplace
                if event.key == pygame.K_r:
                    player.recta.x = 200
                    player.recta.y = 425
                    player.is_jumping = False
                    player.gravity = 0
                    for enemy in enemies:
                        enemy.recta.x = 200
                        enemy.recta.y = 425
                        enemy.is_jumping = False
                        enemy.gravity = 0
                    if player.state != "idle":
                        player.set_state("idle")
                if event.key == pygame.K_9:
                    clear()
                if event.key == pygame.K_1:
                    mousepos = not mousepos

            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                player.jump()

            if (right_pressed) and (not left_pressed):
                player.run()

            if (left_pressed) and (not right_pressed):
                player.walk()

            if event.key == pygame.K_s:
                for enemy in enemies:
                    player.attack(enemy)
                # TODO Iterate over an enemy list

            if control_enemy:
                if event.key == pygame.K_i:
                    for enemy in enemies:
                        enemy.jump()

                if (right_E_pressed) and (not left_E_pressed):
                    for enemy in enemies:
                        enemy.direction = "r"
                        enemy.walk()
                if (left_E_pressed) and (not right_E_pressed):
                    for enemy in enemies:
                        enemy.direction = "l"
                        enemy.walk()

        if event.type == pygame.KEYUP:
            if (left_pressed or right_pressed) and ((not left_held) and (not right_held)):
                player.stop()

            elif (left_held) and (right_pressed):
                player.walk()

            elif (right_held) and (left_pressed) and player.state != "run":
                player.run()

            if control_enemy:
                if (left_E_pressed or right_E_pressed) and ((not left_E_held) and (not right_E_held)):
                    for enemy in enemies:
                        enemy.stop()
                elif (left_E_held) and (right_E_pressed):
                    for enemy in enemies:
                        enemy.direction = "l"
                        enemy.walk()
                elif (right_E_held) and (left_E_pressed):
                    for enemy in enemies:
                        if enemy.state != "run":
                            enemy.direction = "r"
                            enemy.walk()
    # update
    update_start = time.time_ns()

    def update(deltatime):
        global ground_position, bground_position, enemy

        player.update()
        for enemy in enemies:

            enemy.update()

        ground.ground_position, ground.bground_position = ground.scrollmap(
            player, enemies, ground.ground_position, ground.bground_position,
            deltatime)

    now = time.time()
    time_diff = now - previous_time
    previous_time = now
    accumulated_time += time_diff

    update_end = time.time_ns()
    update_time = update_end - update_start

    while accumulated_time >= 0:
        update(deltatime)
        accumulated_time -= deltatime

    # draw
    draw_start = time.time_ns()
    ground.drawbground(screen, ground.bground_position)
    ground.drawground(screen, ground.ground_position)
    player.draw()
    for enemy in enemies:
        enemy.draw()
    draw_time = time.time_ns() - draw_start
    # print(player.x,player.y)
    pygame.display.update()
    clock.tick(FPS)
