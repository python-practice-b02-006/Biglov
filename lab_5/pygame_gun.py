#!/usr/bin/env python3

import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pg.init()

def choose_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

class Ball():
    def __init__(self, coord, vel, rad=20, color=None):
        if color == None:
            color = choose_color()
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad
        self.is_alive = True

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1., g=2.):
        self.vel[1] += int(g * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
               self.is_alive = False

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_perp=1., coef_par=1.):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()


class Table():
    def __init__(self, font_sz=25):
        self.shots = 0
        self.hits = 0
        self.font = pg.font.SysFont("dejavusansmono", font_sz)
        self.margin = 5
    
    def score(self):
        return self.hits - self.shots

    def draw_line(self, screen, text, y, color):
        '''
        draws a line of text with margins, returns y coordinate of the bottom
        '''
        surf = self.font.render(text, True, color)
        screen.blit(surf, [self.margin, y + self.margin])

        return y + surf.get_height() + 2*self.margin
    
    def draw(self, screen):
        y = 0
        y = self.draw_line(screen, "Destroyed: " + str(self.hits), y, WHITE)
        y = self.draw_line(screen, "Used: " + str(self.shots), y, WHITE)
        self.draw_line(screen, "Total: " + str(self.score()), y, RED)





class Gun():
    def __init__(self, coord=[30, SCREEN_SIZE[1]//2], 
                 min_pow=10, max_pow=50):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        end_pos = [self.coord[0] + self.power*np.cos(self.angle), 
                   self.coord[1] + self.power*np.sin(self.angle)]
        pg.draw.line(screen, RED, self.coord, [int(x) for x in end_pos], 5)

    def strike(self):
        vel = [int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)
        
    def move(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1], 
                                mouse_pos[0] - self.coord[0])


class Target():
    def __init__(self, coord, rad=30, color=None):
        if color == None:
            color = choose_color()

        self.coord = coord
        self.rad = rad
        self.color = color
        self.is_alive = True

    def check_collision(self, ball):
        '''
        Checks if the given ball collides with the target
        '''
        R2 = sum([(x - y)**2 for x,y in zip(self.coord, ball.coord)])

        if R2 < (self.rad + ball.rad)**2:
            self.is_alive = False
            return True
        return False

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)
    
class Obstacle:
    def __init__(self, coord, height=30):
        self.coord = coord
        self.beg = coord[0], coord[1] - height//2
        self.end = coord[0], coord[1] + height//2
        self.height = height

        self.is_alive = True

    def draw(self, screen):
        pg.draw.line(screen, WHITE, self.beg, self.end)
        
    def check_collision(self, ball):
        dx = self.coord[0] - ball.coord[0]
        dy = self.coord[1] - ball.coord[1]
        if np.abs(dx) < ball.rad and np.abs(dy) < self.height//2:
            ball.coord[0] += np.sign(ball.vel[0])*(dx - ball.rad)
            ball.vel[0] *= -1

            self.is_alive = False



class Manager():
    def __init__(self, target_count=3, obstacle_count=1):
        self.gun = Gun()
        self.table = Table()
        self.balls = []
        self.targets = []
        self.obstacles = []
        self.target_count = target_count
        self.obstacle_count = obstacle_count


    def new_target(self):
        '''
        add a new target to shoot
        '''
        rad = randint(20, 30)

        x = randint(SCREEN_SIZE[0]//2 + rad, SCREEN_SIZE[0] - rad)
        y = randint(rad, SCREEN_SIZE[1] - rad)

        self.targets.append(Target([x, y], rad))

    def new_obstacle(self):
        '''
        add a new obstacle
        '''
        o_len = 60
        x = randint(SCREEN_SIZE[0]//4, 3*SCREEN_SIZE[0]//4)
        y = randint(o_len//2, SCREEN_SIZE[1] - o_len//2)
        
        self.obstacles.append(Obstacle([x,y], o_len))


    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        self.hits()
        self.draw(screen)
        if self.check_alive():
            for _ in range(self.target_count):
                self.new_target()
            for _ in range(self.obstacle_count):
                self.new_obstacle()

        return done

    def draw(self, screen):
        screen.fill(BLACK)
        for obj_list in (self.balls, self.targets, self.obstacles):
            for obj in obj_list:
                obj.draw(screen)

        self.table.draw(screen)
        self.gun.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()
            for obs in self.obstacles:
                obs.check_collision(ball)
        self.gun.move()

    def hits(self):
        '''
        check for collisions between targets and balls
        '''
        for t in self.targets:
            for b in self.balls:
                if t.check_collision(b):
                    self.table.hits += 1


    def check_alive(self):
        self.balls = [b for b in self.balls if b.is_alive]
        self.targets = [t for t in self.targets if t.is_alive]
        self.obstacles = [o for o in self.obstacles if o.is_alive]
        return len(self.targets) == 0
    
    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.table.shots += 1
        
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Khiryanov")
clock = pg.time.Clock()

mgr = Manager()

done = False

while not done:
    clock.tick(15)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()

