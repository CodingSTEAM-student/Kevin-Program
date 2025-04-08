import pygame
import math
pygame.init()


screen = pygame.display.set_mode((1200, 600))
screen_r = screen.get_rect()
clock = pygame.time.Clock()


car = pygame.image.load("SEPARATED\POLICE_CLEAN_ALLD0036.png")
car_r = car.get_rect(center=screen_r.center)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(car, car_r)
    pygame.display.update()
    clock.tick(30)