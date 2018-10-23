import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from revised_ising_class import *

ising = Ising()
#with open("master.py") as infile:
#    for line in infile:
#        exec(line)

ising.load_table("master")

m_range = np.arange(1,21,1)
n_range = np.arange(1,21,1)

for k in range(1, 21, 1):
	keys = ising.generate_keys(k, k, m_range, n_range)
	sorted_keys = sorted(keys, key = lambda tup : (tup[0], tup[1], tup[2] + tup[3]))
	ising.plot_grids(sorted_keys, k.__str__() + "_plots", 6, (3, 2))
	ising.plot_changes(sorted_keys, k.__str__() + "_changes", 6, (3, 2))