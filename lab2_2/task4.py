#!/usr/bin/env python3

import turtle as ttl

def handle_collision(y, Vy):
    if(y > 0):
        return (y, Vy)
    else:
        return (-y, -Vy)

x = -100
y = 50
Vx = 10
Vy = 0

dt = 0.1

ttl.penup()
ttl.goto(x, y)
ttl.pendown()

while x < 500:
    x += Vx*dt
    y += Vy*dt
    Vy -= 10*dt

    y, Vy = handle_collision(y, Vy)

    ttl.goto(x, y)

