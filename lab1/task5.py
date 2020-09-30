#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def get_approx(xs, ys, deg):
    p, _ = np.polyfit(xs, ys, deg=deg, cov=True)
    return np.poly1d(p)
    

xs = [1, 2, 3, 4, 5]
ys = [0.99, 0.49, 0.35, 0.253, 0.18]

plt.errorbar(xs, ys, xerr=0.05, yerr=0.1, ls='None')

app1 = get_approx(xs, ys, 1)
app2 = get_approx(xs, ys, 2)

pxs = np.arange(1, 5, 0.01)
plt.plot(pxs, app1(pxs), label="linear approximation")
plt.plot(pxs, app2(pxs), label="square approximation")

plt.text(2, 0.7, r'$\mu = \sqrt{\frac{1}{x}}$')

plt.title("График")
plt.xlabel("Ось $x$")
plt.ylabel("Ось $y$")
plt.legend()

plt.show()
