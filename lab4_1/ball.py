#!/usr/bin/env python3
import pygame
from pygame.draw import *
import random as rnd
import numpy as np
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


BALLS = []
MAX_RADIUS = 50
MIN_RADIUS = 10
def add_ball():
    posx = rnd.randint(MAX_RADIUS, screen.get_width() - MAX_RADIUS) 
    posy = rnd.randint(MAX_RADIUS, screen.get_height() - MAX_RADIUS)
    
    phi = 2*rnd.random()*np.pi
    spd_mod = rnd.randint(200, 400)
    spd = int(np.cos(phi)*spd_mod), int(np.sin(phi)*spd_mod)
    
    r = rnd.randint(MIN_RADIUS, MAX_RADIUS)
    color = COLORS[rnd.randint(0, len(COLORS)-1)]
    BALLS.append(((posx, posy), spd, r, color))


def refill_balls(N):
    while len(BALLS) < N:
        add_ball()

def draw_balls():
    for pos, _, r, col in BALLS:
        circle(screen, col, pos, r)

def ball_hit(idx, hit_pos):
    x, y = BALLS[idx][0]
    r = BALLS[idx][2]
    xp, yp = hit_pos

    dx, dy = xp - x, yp - y
    return dx**2 + dy**2 < r**2

TRIANGLES = []
def add_triangle():
    posx = rnd.randint(MAX_RADIUS, screen.get_width() - MAX_RADIUS) 
    posy = rnd.randint(MAX_RADIUS, screen.get_height() - MAX_RADIUS)
    
    phi = 2*rnd.random()*np.pi
    spd_mod = rnd.randint(200, 400)
    spd = int(np.cos(phi)*spd_mod), int(np.sin(phi)*spd_mod)
    
    r = rnd.randint(MIN_RADIUS, MAX_RADIUS)
    color = COLORS[rnd.randint(0, len(COLORS)-1)]
    TRIANGLES.append(((posx, posy), spd, r, color))

def refill_triangles(N):
    while len(TRIANGLES) < N:
        add_triangle()


def draw_triangle(pos, size, color):
    angles = [np.pi/2, np.pi + np.pi/6, -np.pi/6]
    vertices = []
    for a in angles:
        vx = pos[0] + int(np.cos(a)*size)
        vy = pos[1] + int(np.sin(a)*size)
        vertices.append((vx, vy))
    
    polygon(screen, color, vertices)

def draw_triangles():
    for pos, _, r, color in TRIANGLES:
        draw_triangle(pos, r, color)


def update_triangles():
    global TRIANGLES
    F_koef = 1.5
    
    dt = 1/FPS
    new_triangles = []
    for pos, spd, r, color in TRIANGLES:
        x, y = pos
        sx, sy = spd
        
        x += int(sx*dt)
        y += int(sy*dt)

        sx += -sy*F_koef*dt
        sy +=  sx*F_koef*dt

        x, sx = handle_collision(x, screen.get_width(), sx, r)
        y, sy = handle_collision(y, screen.get_height(), sy, r)

        new_triangles.append(((x, y), (sx, sy), r, color))

    TRIANGLES = new_triangles

def triangle_hit(idx, hit_pos):
    x, y = TRIANGLES[idx][0]
    r = TRIANGLES[idx][2]
    xp, yp = hit_pos

    dx, dy = xp - x, yp - y
    return dx**2 + dy**2 < r**2

PENALTY = 20
def handle_click(event):
    global BALLS
    global TRIANGLES
    global MAX_RADIUS
    score_delta = 0
    new_balls = []
    for i in range(len(BALLS)):
        if not ball_hit(i, event.pos):
            new_balls.append(BALLS[i])
        else:
            score_delta += int(PENALTY*(MAX_RADIUS/BALLS[i][2]))
            if(MAX_RADIUS > MIN_RADIUS):
                MAX_RADIUS -= 1
    
    new_triangles = []
    for i in range(len(TRIANGLES)):
        if not triangle_hit(i, event.pos):
            new_triangles.append(TRIANGLES[i])
        else:
            score_delta += int(2*PENALTY*(MAX_RADIUS/TRIANGLES[i][2]))
            if(MAX_RADIUS > MIN_RADIUS):
                MAX_RADIUS -= 1
    
    point_delta = score_delta
    if(point_delta == 0):
        point_delta = -PENALTY

    BALLS = new_balls
    TRIANGLES = new_triangles
    return score_delta, point_delta

def handle_collision(x, max_x, sp_x, r):
    if(x-r < 0):
        x += 2*(r-x)
        sp_x *= -1
    elif(x+r > max_x):
        x -= 2*(x+r - max_x)
        sp_x *= -1

    return x, sp_x


def update_balls():
    global BALLS
    dt = 1/FPS
    new_balls = []
    for pos, spd, r, color in BALLS:
        x, y = pos
        sx, sy = spd
        
        x += int(sx*dt)
        y += int(sy*dt)

        x, sx = handle_collision(x, screen.get_width(), sx, r)
        y, sy = handle_collision(y, screen.get_height(), sy, r)

        new_balls.append(((x, y), (sx, sy), r, color))

    BALLS = new_balls

QUIT_EVENT = False
def game_loop(start_points, balls_number):
    font = pygame.font.SysFont(None, 40)
    points = start_points
    score = 0
    clock = pygame.time.Clock()
    global QUIT_EVENT

    
    pygame.time.set_timer(pygame.NUMEVENTS-1, 1000)
    while (not QUIT_EVENT) and (points > 0):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_EVENT = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sd, pd = handle_click(event)
                score += sd
                points += pd
            elif event.type == pygame.NUMEVENTS-1:
                points -= PENALTY
                    
        refill_balls(balls_number//2)
        update_balls()
        draw_balls()

        refill_triangles(balls_number//2)
        update_triangles()
        draw_triangles()

        img = font.render(str(points), True, BLUE)
        screen.blit(img, (20, 20))

        pygame.display.update()
        screen.fill(BLACK)

    pygame.time.set_timer(pygame.NUMEVENTS-1, 0)
    return score


def do_game_over(t, score):
    font = pygame.font.SysFont(None, 100)
    img = font.render("GAME OVER", True, RED)
    font = pygame.font.SysFont(None, 40)
    img2 = font.render("SCORE: " + str(score), True, RED)
    screen.blit(img , ((screen.get_width() - img.get_width())//2, (screen.get_height() - img.get_height())//2))
    screen.blit(img2, ((screen.get_width() - img2.get_width())//2, (screen.get_height() - img2.get_height())//2 + img.get_height()))
    pygame.display.update()
    pygame.time.wait(t)

LEADERBOARD = []
def load_leaderboard(filename):
    LEADERBOARD.clear()
    with open(filename, 'r') as f:
        for line in f:
            LEADERBOARD.append(int(line))

def save_leaderboard(filename):
    with open(filename, 'w') as f:
        for x in LEADERBOARD:
            print(x, file=f)

def update_leaderboard(score):
    global LEADERBOARD
    LEADERBOARD.append(score)
    LEADERBOARD.sort(key=lambda x: -x)
    LEADERBOARD = LEADERBOARD[0:10]

def draw_leaderboard():
    screen.fill(BLACK)
    y = 20
    
    font = pygame.font.SysFont(None, 60)
    title = font.render("SCOREBOARD", True, RED)
    screen.blit(title, ((screen.get_width() - title.get_width())//2, y))
    y += title.get_height()

    font = pygame.font.SysFont(None, 40)
    for x in LEADERBOARD:
        img = font.render(str(x), True, RED)
        screen.blit(img, ((screen.get_width() - img.get_width())//2, y))
        y += img.get_height()



load_leaderboard("scores.txt")
while not QUIT_EVENT:
    draw_leaderboard()
    pygame.display.update()
    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        QUIT_EVENT = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            score = game_loop(50, 20)
            update_leaderboard(score)
            do_game_over(2000, score)
    
pygame.quit()
save_leaderboard("scores.txt")
