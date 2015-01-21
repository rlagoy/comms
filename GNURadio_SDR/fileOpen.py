#!/usr/bin/python

import numpy as np
import scipy

f=scipy.fromfile(open("IQData1516.bin"), dtype=scipy.complex_)

for x in np.nditer(f):
    print x,
