#!/usr/bin/env python3

import turtle as ttl
import numpy as np

def square(x, y, a):
    ttl.penup()
    ttl.goto(x + a/2, y + a/2)
    ttl.seth(180)
    ttl.pendown()
    
    for i in range(4):
        ttl.fd(a)
        ttl.left(90)

for i in range(1, 11):
    square(0, 0, 10*i)