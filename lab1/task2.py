#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

xs = np.arange(-10, 10, 0.01)
plt.plot(xs, xs*xs - xs - 6)
plt.grid(True)
plt.show()