#!/usr/bin/env python3
import pygame 
from pygame.draw import *
import numpy as np


pygame.init()  
FPS = 30
screen = pygame.display.set_mode((1500, 800))


#house

def draw_background():
    screen.fill([135, 206, 250])
    rect(screen, (66, 189, 84), (0, 400, 1500, 400))

def house(x, y, k):
    """
    Функция house рисует дом.
    х,у - координаты самой левой точки крыши
    k - масштаб домика
    """
    rect(screen, (150, 113, 23), (x, y, int(400*k), int(300*k)))
    rect(screen, (0, 0, 0), (x, y, int(400*k), int(300*k)), int(5*k))
    rect(screen, (95, 158, 169), (x+int(133*k), y+int(100*k), int(133*k), 
                                  int(100*k)))
    rect(screen, (181, 106, 53), (x+int(133*k), y+int(100*k), int(133*k), 
                                  int(100*k)), int(8*k))
    polygon(screen, (246, 74, 70), ((x, y), (x+int(400*k), y), 
                                    (x+int(200*k), y-int(200*k)), (x, y)))
    polygon(screen, (0, 0, 0), ((x, y), (x+int(400*k), y), 
                                (x+int(200*k), y-int(200*k)), (x, y)), 
            int(5*k))


#tree

def tree(x, y, k):
    """
    Функция tree рисует дерево.
    х,у - координаты верхнего левого угла ствола
    k - масштаб дерева
    """
    rect(screen, (0, 0, 0), (x, y, int(50*k), int(250*k)))
    circle(screen, (40, 114, 51), (x+int(20*k), y-int(200*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(20*k), y-int(200*k)), int(80*k), int(3*k))
    circle(screen, (40, 114, 51), (x+int(100*k),y-int(140*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(100*k),y-int(140*k)), int(80*k), int(3*k))
    circle(screen, (40, 114, 51), (x-int(65*k), y-int(140*k)), int(80*k))
    circle(screen, (0, 0, 0), (x-int(65*k), y-int(140*k)), int(80*k), int(3*k))
    circle(screen, (40, 114, 51), (x+int(20*k), y-int(110*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(20*k), y-int(110*k)), int(80*k), int(3*k))
    circle(screen, (40, 114, 51), (x-int(40*k), y-int(50*k)), int(80*k))
    circle(screen, (0, 0 ,0), (x-int(40*k), y-int(50*k)), int(80*k), int(3*k))
    circle(screen, (40, 114, 51), (x+int(80*k), y-int(50*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(80*k), y-int(50*k)), int(80*k), int(3*k))
    
    
#cloud

def cloud(x, y, k):
    """
    Функция cloud рисует облако.
    x,y - координаты центра первой окружности нарисованного облачка
    k - масштаб
    """
    circle(screen, (255, 255, 255), (x, y), int(80*k))
    circle(screen, (0, 0, 0), (x, y), int(80*k), int(3*k))
    circle(screen, (255, 255, 255), (x+int(90*k), y), int(80*k))
    circle(screen, (0, 0, 0), (x+int(90*k), y), int(80*k), int(3*k))
    circle(screen, (255, 255, 255), (x+int(180*k), y), int(80*k))
    circle(screen, (0, 0, 0), (x+int(180*k), y), int(80*k), int(3*k))
    circle(screen, (255, 255, 255), (x+int(270*k), y), int(80*k))
    circle(screen, (0, 0, 0), (x+int(270*k), y), int(80*k), int(3*k))
    circle(screen, (255, 255, 255), (x+int(190*k), y-int(70*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(190*k), y-int(70*k)), int(80*k), int(3*k))
    circle(screen, (255, 255, 255), (x+int(85*k), y-int(70*k)), int(80*k))
    circle(screen, (0, 0, 0), (x+int(85*k), y-int(70*k)), int(80*k), int(3*k))
    
    
#sun

def sun(x, y, k):
    """
    Фунция sun рисует солнце.
    x,y - координаты центра солнца
    k - масштаб солнца
    """
    circle(screen, (255, 255, 0), (x, y), int(50*k))
    n = 20
    for i in range(0, n, 1):
        alpha = 2*np.pi/n
        x1 = x + 50*k*np.cos(i*alpha)
        y1 = y + 50*k*np.sin(i*alpha)
        x2 = x + 50*k*np.cos((i+0.6)*alpha)
        y2 = y + 50*k*np.sin((i+0.6)*alpha)
        x3 = x + 60*k*np.cos((i+0.3)*alpha)
        y3 = y + 60*k*np.sin((i+0.3)*alpha)
        polygon(screen, (255, 255, 0), ((x1,y1), (x2, y2), (x3, y3)))
        
def draw_static():
    house(900, 430, 0.5)
    house(200, 450, 0.8)
    tree(650, 450, 0.7)
    tree(1200, 430, 0.5) 

CLOUDS = [
    (800, 250, 0.4),
    (1200, 150, 0.5),
    (350, 150, 0.6)
]

def draw_clouds():
    for x, y, k in CLOUDS:
        cloud(x, y, k)

cloud_speed = 0.6
def update_clouds(dt):
    for i, t in enumerate(CLOUDS):
        x, y, k = t
        spd = cloud_speed*k
        x = int(x - spd*dt)
        if x < -400*k:
            x = screen.get_width()

        CLOUDS[i] = x, y, k
        
clock = pygame.time.Clock()
finished = False


time = pygame.time.get_ticks()
while not finished:
    clock.tick(FPS)
    update_clouds(pygame.time.get_ticks() - time)
    time = pygame.time.get_ticks()

    draw_background()
    sun(100, 100, 1)
    draw_clouds()
    draw_static()
    pygame.display.update()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
