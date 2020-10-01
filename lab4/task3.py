#!/usr/bin/env python3

# Task 9_1 chosen by RNG

import pygame
import numpy as np
import pygame.draw as dr
import pygame.transform as trans

COLORS = {
    "grey": (230, 230, 230),
    "dark-grey": (50, 50, 50),
    "water": (22, 80, 68),
    "black": (0, 0, 0),
    "sky": (0, 255, 255)
}




def bordered_ellipse(screen, color, rect, width):
    dr.ellipse(screen, color, rect)
    dr.ellipse(screen, COLORS["black"], rect, width)

def draw_sun(screen):
    width = screen.get_width()

    srf = pygame.Surface((width//2, width//2))
    srf.set_colorkey((0, 0, 0))

    dr.ellipse(srf, (255, 255, 255), [0, 0, width//2, width//2], 20)
    dr.ellipse(srf, (255, 255, 255), [width//4 - 20, width//4 - 20, 40, 40])
    dr.rect(srf, (255, 255, 255), [width//4 - 5, 0, 10, width//2])
    dr.rect(srf, (255, 255, 255), [0, width//4 - 5, width//2, 10])
    
    screen.blit(srf, (width//2, 0))



def draw_background(screen):
    width, height = screen.get_width(), screen.get_height()

    screen.fill(COLORS["sky"])
    dr.rect(screen, COLORS["grey"], [0, height//2, width, height//2])
    dr.line(screen, COLORS["black"], (0, height//2), (width, height//2))

    draw_sun(screen)



def draw_poodle(screen, x, y, scale):
    w, h = int(100*scale), int(50*scale)

    rect1 = [x - w//2, y - h//2, w, h]
    bordered_ellipse(screen, COLORS["dark-grey"], rect1, 2)

    w2, h2 = 3*w//4, 3*h//4
    rect2 = [x - w2//2, y + h//2 - h2, w2, h2]
    bordered_ellipse(screen, COLORS["water"], rect2, 2)




def draw_bear_head(screen, x, y, scale):
    w, h = 100*scale, 60*scale
    rect = [int(c) for c in [x - w//2, y - h//2, w, h]]
    
    # base
    bordered_ellipse(screen, COLORS["grey"], rect, 2)

    # eye and nose
    dr.ellipse(screen, COLORS["black"], [x - w//6, y - h//5, w//8, h//8])
    dr.ellipse(screen, COLORS["black"], [x + 4*w//9, y - h//7, w//8, h//8])

    # mouth
    m_w, m_h = int(w*1.1), h//4
    dx, dy = int(-7*scale), int(3*scale)
    mouth_rect = [x - m_w//2 + dx, y - m_h//2 + dy, m_w, m_h]
    dr.arc(screen, COLORS["black"], mouth_rect, 3*np.pi/2, 2*np.pi)

    #ear
    e_x, e_y = x - 3*w//9, y - 3*h//9
    e_w, e_h = w//5, h//5

    ear_rect1 = [e_x - e_w//2, e_y - e_h//2, e_w, e_h]
    ear_rect2 = [e_x - e_w//2, e_y - e_h, e_w, e_h*2]
    dr.ellipse(screen, COLORS["grey"], ear_rect1)
    dr.arc(screen, COLORS["black"], ear_rect1, 0, 1.1*np.pi, 2)
    dr.arc(screen, COLORS["black"], ear_rect2, 1.05*np.pi, 2*np.pi, 2)

def draw_pole(screen, x, y, scale):
    segment_len = int(60*scale)
    segment_ang = [-np.pi/3, -np.pi/4, -np.pi/4 - 0.05, -np.pi/4 + 0.05, -np.pi/4]
    width = 6*scale

    x_c, y_c = x, y
    for ang in segment_ang:
        dx, dy = int(segment_len*np.cos(ang)), int(segment_len*np.sin(ang))
        dr.line(screen, COLORS["black"], (x_c, y_c), (x_c+dx, y_c+dy), width)

        x_c += dx
        y_c += dy

    ye = y + segment_len
    dr.line(screen, COLORS["black"], (x_c, y_c), (x_c, ye))
    


def draw_bear(screen, x, y, scale):
    w, h = int(180*scale), int(300*scale)
    
    draw_bear_head(screen, x + w//4, y -6*h//11, scale)


    #body
    bordered_ellipse(screen, COLORS["grey"], [x - w//2, y - h//2, w, h], 2)

    #legs
    bordered_ellipse(screen, COLORS["grey"], [x, y + h//4, w//2, h//4], 2)
    bordered_ellipse(screen, COLORS["grey"], [x + w//4, y + 3*h//7, w//2, h//10], 2)


    #fishing pole
    draw_pole(screen, x + 6*w//10, y - h//14, scale)

    #arms
    bordered_ellipse(screen, COLORS["grey"], [x + w//3, y - h//4, w//2, h//16], 2)

def draw_fish(screen, x, y, ang, scale, mirror):
    srf = FISH_IMG.copy()

    srf = trans.rotate(srf, ang)
    srf = trans.scale(srf, (int(srf.get_width()*scale), int(srf.get_height()*scale)))
    if mirror:
        srf = trans.flip(srf, True, False)

    screen.blit(srf, (x, y))

def draw_fishes(screen, x, y, scale):
    dl = int(10*scale)
    coords = [
        ( 4, 5, 10, scale/3, False),
        (-2, 4,-10, scale/3, False),
        ( 5, 6,-10, scale/3, True),
        (-1, 8,-10, scale/3, False),

        ( 1,-5, 10, scale/4, True),
        ( 4,-5,  0, scale/4, False),
        ( 7,-5,-10, scale/4, False)
    ]

    for dx, dy, ang, scl, mirr in coords:
        draw_fish(screen, x + dx*dl, y + dy*dl, ang, scl, mirr)

def draw_scene(screen, x, y, scale):
    draw_poodle(screen, x + 125*scale, y + 40*scale, 1.5*scale)
    draw_bear(screen, x - 180*scale, y, scale)
    draw_fishes(screen, x, y, scale)

def get_scene_srf():
    scene_srf = pygame.Surface((600, 900))
    scene_srf.set_colorkey((0, 255, 0))
    scene_srf.fill((0, 255, 0))
    draw_scene(scene_srf, scene_srf.get_width()//2, scene_srf.get_height()//2, 1)

    return scene_srf

def draw_scenes(screen):
    scene_srf = get_scene_srf()

    coords = [
        (100, 400, 0.4, True),
        (350, 300, 0.4, True),
        (  0, 500, 0.6, False),
        (200, 300, 0.8, True)
    ]

    for x, y, scale, mirr in coords:
        w, h = int(scale*scene_srf.get_width()), int(scale*scene_srf.get_height())
        srf = trans.scale(scene_srf, (w, h))
        srf = trans.flip(srf, mirr, False)

        screen.blit(srf, (x,y))



pygame.init()
FISH_IMG = pygame.image.load("fish.png")

FPS = 30
screen = pygame.display.set_mode((600, 900))


draw_background(screen)
draw_scenes(screen)

pygame.display.update()


clock = pygame.time.Clock()

finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()