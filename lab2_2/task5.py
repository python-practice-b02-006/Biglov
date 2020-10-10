#!/usr/bin/env python3

import turtle as ttl
import random as rnd
import numpy as np

N = 10
TTL = [ttl.Turtle(shape='turtle') for i in range(N)]
POS = [(rnd.random(),rnd.random()) for i in range(N)]
SPD = [(rnd.random()*10,rnd.random()*10) for i in range(N)]
dt = 0.0001

def update_pos():
    for i in range(N):
        x, y = POS[i]
        Vx, Vy = SPD[i]

        POS[i] = x + Vx*dt, y + Vy*dt


def calc_f(t_id):
    fx, fy = 0, 0
    x0, y0 = POS[t_id]
    for i, t in enumerate(POS):
        if i == t_id:
            continue

        x, y = t
        dx = x0 - x 
        dy = y0 - y 
        r = np.sqrt(dx**2 + dy**2)

        fx += 100*dx/r**3
        fy += 100*dy/r**3

    return fx, fy

def update_speeds():
    new_speeds = []
    for i, t in enumerate(SPD):
        fx, fy = calc_f(i)

        sx, sy = t

        sx += fx*dt
        sy += fy*dt

        new_speeds.append((sx,sy))
        print()

    return new_speeds

def single_collision_handling(x, Vx):
    if(x <= 0):
        return -x, -Vx
    if(x > 1):
        return 2-x, -Vx
    return x, Vx



def handle_collisions():
    for i in range(N):
        x, y = POS[i]
        Vx, Vy = SPD[i]

        x, Vx = single_collision_handling(x, Vx)
        y, Vy = single_collision_handling(y, Vy)

        POS[i] = (x, y)
        SPD[i] = (Vx, Vy)

DRAW_KOEFF = 500
def draw_turtles():
    for unit, pos in zip(TTL, POS):
        x, y = pos 
        k = DRAW_KOEFF
        unit.goto(x*k - k/2, y*k - k/2)

def get_kinetic():
    return sum(x**2 + y**2 for x,y in SPD)

for unit in TTL:
    unit.penup()
    unit.speed(0)
    unit.shape("circle")
    unit.resizemode("user")
    unit.turtlesize(0.5, 0.5)


steps = 300
add_s = 2

kinetic_data = []
for i in range(steps):
    draw_turtles()
    kinetic_data.append(get_kinetic())
    for i in range(add_s):
        new_SPD = update_speeds()
        update_pos()
        SPD = new_SPD

        handle_collisions()

with open("kinetic.txt", 'w') as f:
    for x in kinetic_data:
        print(x, file=f)
    

