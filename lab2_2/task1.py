#!/usr/bin/env python3

import turtle as ttl
import random as rnd

def move_turtle(avg_len):
    ttl.seth(360*rnd.random())
    ttl.forward(2*avg_len*rnd.random())

step = 20
for i in range(100):
    move_turtle(step)

