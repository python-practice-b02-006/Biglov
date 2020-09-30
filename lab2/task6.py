#!/usr/bin/env python3

import turtle as ttl
import numpy as np

def spider(r, n):
    for i in range(n):
        phi = i*360/n
        
        ttl.seth(phi)
        ttl.fd(r)
        ttl.stamp()
        ttl.bk(r)
        

spider(50, 12)