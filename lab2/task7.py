#!/usr/bin/env python3

import turtle as ttl
import numpy as np

steps = 200
nrot = 8
k = 3

for i in range(steps):
    phi = 2*nrot*np.pi*i/steps

    ttl.goto(k*phi*np.cos(phi), k*phi*np.sin(phi))

