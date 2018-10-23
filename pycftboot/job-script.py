# This is the script for one job instance, parametrized by $SGE_TASK_ID.
import bootstrap
import matplotlib
matplotlib.use('TkAgg')   # generate postscript output by default
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from revised_ising_gap import *
import sys

# Read the arguments given and assign them their correct variables names.
# First argument will be $SGE_TASK_ID.
SGE_TASK_ID = sys.argv[1]
k_start = sys.argv[2]
k_stop = sys.argv[3]
l_start = sys.argv[4]
l_stop = sys.argv[5]
m_start = sys.argv[6]
m_stop = sys.argv[7]
n_start = sys.argv[8]
n_stop = sys.argv[9]

# Convert these raw numbers into Python lists.
if k_stop - k_start == 0:
	k_range = [k_start]
else:
	k_range = np.arange(k_start, k_stop + 1, 1).tolist()
if l_stop - l_start == 0:
	l_range = [l_start]
else:
	l_range = np.arange(l_start, l_stop + 1, 1).tolist()
if m_stop - m_start == 0:
	m_range = [m_start]
else:
	m_range = np.arange(m_start, m_stop + 1, 1).tolist()
if n_stop - n_start == 0:
	n_range = [n_start]
else:
	n_range = np.arange(n_start, n_stop + 1, 1).tolist()

# Instantiate an ising_gap object, which has default dim, gap, sig_values, eps_values & 'cutoff'.
ising_gap = Ising_Gap()

# Generate all specified grids, store them in the class 'table' attribute.
ising_gap.iterate_parameters(k_range, l_range, m_range, n_range)

# Save the contents of 'table' to an executable python file, 
ising_gap.save_to_file(SGE_TASK_ID.__str__())