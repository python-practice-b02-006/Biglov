#!/usr/bin/env python3

import numpy as np

def y_func(x: float):
    num = np.exp(1/(np.sin(x) + 1))
    den = (5/4 + 1/x**15)
    return np.log(num/den)/np.log(1 + x**2)

for x in 1, 10, 1000:
    print(y_func(x), end=" ")
print()