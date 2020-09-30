#!/usr/bin/env python3

import turtle as ttl
import numpy as np

ttl.shape('turtle')
ttl.penup()
ttl.goto(50, 0)
ttl.pendown()
for i in range(0, 100):
    phi = 2*np.pi*i/100
    ttl.goto(50*np.cos(phi), 50*np.sin(phi))