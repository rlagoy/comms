#!/usr/bin/python

import numpy as np
import scipy

f=scipy.fromfile(open("fskData.bin"), dtype=scipy.byte)

for x in np.nditer(f):
    print x,
