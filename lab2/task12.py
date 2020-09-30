#!/usr/bin/env python3

import turtle as ttl
import numpy as np

def arc(x, y, r, phi1, phi2):
    ttl.penup()
    ttl.goto(x + r*np.cos(phi1), y + np.sin(phi1))
    ttl.pendown()

    steps = 100
    for i in range(1, steps+1):
        phi = ((steps-i)*phi1 + i*phi2)/steps
        ttl.goto(x + r*np.cos(phi), y + r*np.sin(phi))


n = 5
R = 20
r = 5


for i in range(n):
    xR = i*2*(R-r)
    xr = xR + R - r

    arc(xR, 0, R,   np.pi, 0)
    arc(xr, 0, r, 2*np.pi, np.pi)

arc(n*2*(R-r), 0, R,   np.pi, 0)