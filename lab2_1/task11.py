#!/usr/bin/env python3

import turtle as ttl
import numpy as np

def circle(x, y, r):
    ttl.penup()
    ttl.goto(x+r, y)
    ttl.pendown()

    steps = 100
    for i in range(1, steps+1):
        phi = 2*np.pi*i/steps
        ttl.goto(x + r*np.cos(phi), y + r*np.sin(phi))


step = 10
start = 20
n = 6

for r in range(start, start + n*step, step):
    circle( r, 0, r)
    circle(-r, 0, r)