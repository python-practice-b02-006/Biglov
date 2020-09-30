#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def y_func(x):
    base = 1 + np.tan(1/(1 + np.sin(x)**2))
    return np.log(x*x + 1)/np.log(base) * np.exp(-np.abs(x)/10)

xs = np.arange(-20, 20, 0.01)
plt.plot(xs, y_func(xs))
plt.grid(True)
plt.show()