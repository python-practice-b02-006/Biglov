#!/usr/bin/env python3
import turtle as ttl
import numpy as np

def star(n, r):
    alpha = 180/n
    len = 2*(r*np.cos((alpha/2)/180*np.pi))
    print(len)

    ttl.penup()
    ttl.goto(r, 0)
    ttl.pendown()

    ttl.seth(180 - alpha/2)


    for i in range(n):
        ttl.forward(len)
        ttl.left(180 - alpha)


star(11, 40)
star(5, 100)