#!/usr/bin/env python3

import turtle as ttl
import numpy as np

def npoly(n, r):
    ttl.penup()
    ttl.goto(r, 0)
    ttl.pendown()

    for i in range(1, n+1):
        phi = 2*np.pi*i/n
        ttl.goto(r*np.cos(phi), r*np.sin(phi))
    

step = 20
for i in range(3, 14):
    npoly(i, i*step)