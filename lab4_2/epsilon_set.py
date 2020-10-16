#!/usr/bin/env python3
import math

class eps_set(set):
    def __init__(self, eps, iterable=[]):
        self.eps = eps
        for x in iterable:
            self.add(x)

    def add(self, elem):
        for x in self:
            if(abs(x-elem) < self.eps):
                return
        
        set.add(self, elem)

s = eps_set(2, [1,2,3])
print(s)

for x in range(20):
    s.add(x)

print(s)