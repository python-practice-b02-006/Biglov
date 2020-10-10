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

ttl.begin_fill()
arc(0, 0, 100, 0, 2*np.pi)
ttl.fillcolor("yellow")
ttl.end_fill()

ttl.begin_fill()
arc(40, 30, 10, 0, 2*np.pi)
ttl.fillcolor("blue")
ttl.end_fill()

ttl.begin_fill()
arc(-40, 30, 10, 0, 2*np.pi)
ttl.fillcolor("blue")
ttl.end_fill()

ttl.width(10)

ttl.penup()
ttl.goto(0, 10)
ttl.pendown()
ttl.seth(270)
ttl.fd(25)

ttl.color("red")
arc(0, -15, 20, np.pi, 2*np.pi)