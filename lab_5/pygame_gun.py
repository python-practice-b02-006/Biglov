#!/usr/bin/env python3

import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pg.init()

def choose_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

class Ball():
    def __init__(self, coord, vel, rad=15, color=None):
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
    pass


class Gun():
    def __init__(self, coord=[30, SCREEN_SIZE[1]//2], 
                 min_pow=10, max_pow=30):
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
    



class Manager():
    def __init__(self, target_count=3):
        self.gun = Gun()
        self.table = Table()
        self.balls = []
        self.targets = []
        self.target_count = target_count


    def new_target(self):
        '''
        add a new target to shoot
        '''
        rad = randint(20, 30)

        x = randint(rad, SCREEN_SIZE[0] - rad)
        y = randint(rad, SCREEN_SIZE[1] - rad)

        self.targets.append(Target([x, y], rad))

    
    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        self.draw(screen)
        if self.check_alive():
            for i in range(self.target_count):
                self.new_target()

        return done

    def draw(self, screen):
        screen.fill(BLACK)
        for ball in self.balls:
            ball.draw(screen)

        for targ in self.targets:
            targ.draw(screen)

        self.gun.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()
        self.gun.move()

    def check_alive(self):
        self.balls = [b for b in self.balls if b.is_alive]
        self.targets = [t for t in self.targets if t.is_alive]
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

