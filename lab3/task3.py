#!/usr/bin/env python3

import turtle as ttl

DIGIT_PATTERNS = []

def print_digit(dig, x0, y0, size):
    vert = DIGIT_PATTERNS[dig]
    
    ttl.penup()
    xv, yv = vert[0]
    ttl.goto(x0 + xv*size, y0 + yv*size)
    ttl.pendown()
    for x, y in vert:
        print(x, y)
        ttl.goto(x0 + x*size, y0 + y*size) 

def read_font(filename):
    DIGIT_PATTERNS.clear()
    with open(filename, "r") as f:
        for line in f:
            DIGIT_PATTERNS.append(eval(line))


def write_font(filename):
    with open(filename, "w") as f:
        for dig in DIGIT_PATTERNS:
            print(repr(dig), file=f)

read_font("font.txt")

size = 30
digits = [1, 4, 1, 7, 0, 0]
for i, d in  enumerate(digits):
    print_digit(d, i*size*2, 0, size)