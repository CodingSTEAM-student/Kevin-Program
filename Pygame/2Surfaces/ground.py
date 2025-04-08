import pygame
from pygame.image import load as load_image 

#Ground code        
def moveground(ground_position, ground_speed):
    ground_x,ground_x2 = ground_position
    ground_x -= ground_speed
    if ground_x <= -1345 or ground_x>screenW:
        ground_x=0
    ground_x2=ground_x
    if ground_x<=0:
        ground_x2+=1345
    else: 
        ground_x2-=1345
    return ground_x, ground_x2
def drawground(screen,ground_position):
    ground_x,ground_x2 = ground_position
    screen. blit(g,(ground_x, 425) )
    if DEBUGGER:
        pygame.draw.rect(screen,"red",g.get_rect(topleft=(ground_x ,425)),2)
    screen. blit(g,(ground_x2, 425))
def movebground(bground_position, bground_speed):
    bground_x,bground_x2 = bground_position
    bground_x -= bground_speed
    if bground_x < screenW-b.get_width()*2:
        bground_x=0
    if bground_x>0:
        bground_x=-b.get_width()
    # bground_x2=bground_x
    #=bground_x2
    # if bground_x<=0:
    #     bground_x2+=b.get_width()
    # else: 
    #     bground_x2-=b.get_width()
    return bground_x, bground_x+b.get_width()
def drawbground(screen,bground_position):
    bground_x,bground_x2 = bground_position
    screen. blit(b,(bground_x, 0))
    if DEBUGGER:
        pygame.draw.rect(screen,"red",b.get_rect(topleft=(bground_x, 0)),2)
    screen. blit(b,(bground_x2, 0))

def scrollmap(player,enemies,ground_position,bground_position,deltatime):
    if player.recta.x>=725 and player.speed>0:
        ground_position=moveground(ground_position, 3)
        bground_position=movebground(bground_position, 3)
        player.move(False)

        for enemy in enemies:
            enemy.checkscroll(3)
    elif player.recta.x<=75 and player.speed<0:
        ground_position=moveground(ground_position, -2)
        bground_position=movebground(bground_position, -2)
        player.move(False)
        for enemy in enemies:
            enemy.checkscroll(-2)
    return ground_position,bground_position 

g=load_image("graphics/desert_ground.png")
b= load_image("graphics/background.png")
b1=pygame.transform.flip(b,True,False)
DEBUGGER=None
screenW=None
screenH=None
ground_position = (0, 0)
bground_position=(0,b.get_width())