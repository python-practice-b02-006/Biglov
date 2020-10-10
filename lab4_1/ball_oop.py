#!/usr/bin/env python3
import pygame
import pygame.draw as dr 
import random as rnd
import numpy as np
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))
font_big = pygame.font.SysFont(None, 100)
font_mid = pygame.font.SysFont(None, 60)
font_sml = pygame.font.SysFont(None, 40)
SCORE_STEP = 20

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def handle_collision(x, max_x, sp_x, r):
    if(x-r < 0):
        x += 2*(r-x)
        sp_x *= -1
    elif(x+r > max_x):
        x -= 2*(x+r - max_x)
        sp_x *= -1

    return x, sp_x

def check_hit(obj, hit_pos):
    x, y = obj.pos
    hx, hy = hit_pos

    dx, dy = x - hx, y - hy
    return dx**2 + dy**2 < obj.size**2

class Ball:
    def __init__(self):
        self.pos = 0, 0
        self.spd = 0, 0
        self.size = 0
        self.color = BLACK

    def update(self, dt):
        x, y = self.pos
        vx, vy = self.spd

        x += vx*dt
        y += vy*dt

        x, vx = handle_collision(x, screen.get_width(),  vx, self.size)
        y, vy = handle_collision(y, screen.get_height(), vy, self.size)

        self.pos = int(x), int(y)
        self.spd = vx, vy

    def draw(self):
        dr.circle(screen, self.color, self.pos, self.size)



class Triangle:
    F_koef = 1.5

    def __init__(self):
        self.pos = 0, 0
        self.spd = 0, 0
        self.size = 0
        self.color = BLACK

    def update(self, dt):
        x, y = self.pos
        vx, vy = self.spd

        x += vx*dt
        y += vy*dt

        vx -= vy*dt*self.F_koef
        vy += vx*dt*self.F_koef

        x, vx = handle_collision(x, screen.get_width(),  vx, self.size)
        y, vy = handle_collision(y, screen.get_height(), vy, self.size)

        self.pos = int(x), int(y)
        self.spd = vx, vy

    def draw(self):
        angles = [np.pi/2, np.pi + np.pi/6, -np.pi/6]
        vertices = []
        for a in angles:
            vx = self.pos[0] + int(np.cos(a)*self.size)
            vy = self.pos[1] + int(np.sin(a)*self.size)
            vertices.append((vx, vy))
        
        dr.polygon(screen, self.color, vertices)


class Session:
    def generate_params(self):
        posx = rnd.randint(self.max_radius, screen.get_width()  - self.max_radius) 
        posy = rnd.randint(self.max_radius, screen.get_height() - self.max_radius)
        
        phi = 2*rnd.random()*np.pi
        spd_mod = rnd.randint(200, 400)
        spd = int(np.cos(phi)*spd_mod), int(np.sin(phi)*spd_mod)
        
        r = rnd.randint(self.min_radius, self.max_radius)
        color = COLORS[rnd.randint(0, len(COLORS)-1)]
        return (posx, posy), spd, r, color

    def generate_obj(self, obj_type):
        res = obj_type()
        res.pos, res.spd, res.size, res.color = self.generate_params()
        return res
    
    def refill_objects(self):
        while len(self.balls) < self.ball_count:
            self.balls.append(self.generate_obj(Ball))
    
        while len(self.triangles) < self.triangle_count:
            self.triangles.append(self.generate_obj(Triangle))
    
    def update_objects(self, dt):
        for obj in self.balls:
            obj.update(dt)
        for obj in self.triangles:
            obj.update(dt)

    def draw_objects(self):
        for obj in self.balls:
            obj.draw()
        for obj in self.triangles:
            obj.draw()
    
    def object_score(self, obj):
        res = int(SCORE_STEP*self.max_radius/obj.size)
        if isinstance(obj, Triangle):
            res *= 2
        
        return res

    def handle_click_list(self, obj_list, event):
        new_list = []
        score = 0

        for obj in obj_list:
            if not check_hit(obj, event.pos):
                new_list.append(obj)
            else:
                score += self.object_score(obj)
                if self.max_radius > self.min_radius:
                    self.max_radius -= 1

        obj_list[:] = new_list
        return score

    def handle_click(self, event):
        score =  self.handle_click_list(self.triangles, event)
        score += self.handle_click_list(self.balls, event)

        points = score
        if(points == 0):
            points -= SCORE_STEP
        return score, points
        

    def __init__(self, min_radius, max_radius, ball_count, triangle_count):
        self.min_radius = min_radius
        self.max_radius = max_radius

        self.ball_count = ball_count
        self.triangle_count = triangle_count

        self.balls = []
        self.triangles = []
        self.refill_objects()




QUIT_EVENT = False
def game_loop(start_points, balls_count, triangles_count):
    global QUIT_EVENT
    font = pygame.font.SysFont(None, 40)
    points = start_points
    score = 0
    clock = pygame.time.Clock()
    session = Session(10, 50, balls_count, triangles_count)
    

    
    pygame.time.set_timer(pygame.NUMEVENTS-1, 1000)
    while (not QUIT_EVENT) and (points > 0):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT_EVENT = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sd, pd = session.handle_click(event)
                score += sd
                points += pd
            elif event.type == pygame.NUMEVENTS-1:
                points -= SCORE_STEP
                    
        session.refill_objects()
        session.update_objects(1/FPS)
        session.draw_objects()

        img = font.render(str(points), True, BLUE)
        screen.blit(img, (20, 20))

        pygame.display.update()
        screen.fill(BLACK)

    pygame.time.set_timer(pygame.NUMEVENTS-1, 0)
    return score

def draw_text(text, font, y):
    img = font.render(text, True, RED)
    x0, y0 = (screen.get_width() - img.get_width())//2, y - img.get_height()//2
    screen.blit(img, (x0, y0))

    return y0, img.get_height()

def do_game_over(t, score):
    y, dy = draw_text("GAME OVER", font_big, screen.get_height()//2)
    draw_text("YOUR SCORE: " + str(score), font_sml, y+dy + font_sml.size("Y")[1]//2)

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
    
    y, dy = draw_text("SCOREBOARD", font_mid, y + font_mid.size("S")[1]//2)
    y += dy

    for x in LEADERBOARD:
        y, dy = draw_text(str(x), font_sml, y + font_sml.size("1")[1]//2)
        y += dy


load_leaderboard("scores.txt")
while not QUIT_EVENT:
    draw_leaderboard()
    pygame.display.update()
    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        QUIT_EVENT = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            score = game_loop(50, 15, 10)
            update_leaderboard(score)
            do_game_over(2000, score)
    
pygame.quit()
save_leaderboard("scores.txt")

