#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def get_ys(xs, func_str):
    ys = np.empty(xs.size)
    for i in range(xs.size):
        ys[i] = eval(func_str, globals(), {'x': xs[i]})
    return ys


func_str = input()

xs = np.arange(-5, 5, 0.01)
with plt.xkcd():
    plt.plot(xs, get_ys(xs, func_str))
    plt.show()
