from __future__ import division
from numba import cuda
import numpy as np
import math


@cuda.jit
def krn(a,b):
    position = cuda.grid(1)
    if position < b.size:
        a[position] *= b[position]
