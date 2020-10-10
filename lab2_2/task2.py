#!/usr/bin/env python3

import turtle as ttl

DIGIT_PATTERNS = [
    [(0, 0), (0, 2), (1, 2), (1, 0), (0, 0)],
    [(0, 1), (1, 2), (1, 0)],
    [(0, 2), (1, 2), (1, 1), (0, 0)],
    [(0, 0), (1, 1), (0, 1), (1, 2), (0, 2)],
    [(0, 2), (0, 1), (1, 1), (1, 2), (1, 0)],
    [(1, 2), (0, 2), (0, 1), (1, 1), (1, 0), (0, 0)],
    [(1, 2), (0, 1), (1, 1), (1, 0), (0, 0), (0, 1)],
    [(0, 0), (0, 1), (1, 2), (0, 2)],
    [(0, 0), (0, 2), (1, 2), (0, 2), (0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 1), (0, 1), (0, 2), (1, 2), (1, 1)]
]

def print_digit(dig, x0, y0, size):
    vert = DIGIT_PATTERNS[dig]
    
    ttl.penup()
    xv, yv = vert[0]
    ttl.goto(x0 + xv*size, y0 + yv*size)
    ttl.pendown()
    for x, y in vert:
        print(x, y)
        ttl.goto(x0 + x*size, y0 + y*size) 


size = 30
digits = [1, 4, 1, 7, 0, 0]
for i, d in  enumerate(digits):
    print_digit(d, i*size*2, 0, size)