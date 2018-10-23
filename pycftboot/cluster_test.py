import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from revised_ising_gap import *


kmax = [7,8]
lmax = [7,8]
mmax = np.arange(2, 21, 1).tolist()
nmax = np.arange(2, 21, 1).tolist()

ising_gap = IsingGap()

ising_gap.iterate_parameters(kmax, lmax, mmax, nmax)

ising_gap.save_to_file("simple_test")