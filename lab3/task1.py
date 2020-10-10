#!/usr/bin/env python3

import pygame
import numpy as np
import pygame.draw as dr


def draw_eye(x, y, size, inner_size):
    dr.circle(screen, (255, 0, 0), (x,y), size)
    dr.circle(screen, (0, 0, 0), (x,y), size, 1)
    dr.circle(screen, (0, 0, 0), (x,y), inner_size)

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    
    return int(qx), int(qy)

def rotate_rect(rect, angle):
    x, y, w, h = rect
    origin = (x + w/2, y + h/2)

    res = []
    pts = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    for p in pts:
        res.append(rotate(origin, p, angle))

    return res



pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((180,180,180))

dr.circle(screen, (255, 255, 0), (200,200), 100)
dr.circle(screen, (0, 0, 0), (200,200), 100, 1)

dr.rect(screen, (0, 0, 0), (150, 250, 100, 20))

draw_eye(150, 170, 25, 10)
draw_eye(250, 170, 20, 10)

dr.polygon(screen, (0,0,0), rotate_rect((100, 130, 100, 10), np.pi/6))
dr.polygon(screen, (0,0,0), rotate_rect((210, 130, 100, 10), -np.pi/6))

pygame.display.update()
clock = pygame.time.Clock()

finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()