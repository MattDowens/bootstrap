<<<<<<< HEAD
import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from new_ising_class import *
import sys

# Generate grid of points and row_lists, to index in determine_points
sig_step = 0.0005
eps_step = 0.005

v1 = [0, eps_step]
v2 = [sig_step, sig_step]

start = [0.516, 1.39]
stop = [0.523, 1.44]

sig_range = np.arange(start[0], stop[0] + sig_step, sig_step)
eps_range = np.arange(start[1], stop[1] + eps_step, eps_step)

sig_start = start[0]
eps_start = start[1]

sig_values = []
eps_values = []

row_lists = []
sig_row_start = sig_start
eps_row_start = eps_start
sigs = []
eps = []
for r in range(len(eps_range)):
	row_lists.append([])
	for s in range(len(sig_range)):
		sigs.append(sig_row_start + s * v2[0])
		eps.append(eps_row_start + s * v2[1])
		sig_values.append(sig_row_start + s * v2[0])
		eps_values.append(eps_row_start + s * v2[1])
	row_lists[r].append(sigs)
	row_lists[r].append(eps)
	sigs = []
	eps = []
	# Alter the starting position of the next row.
	if r!= len(eps_range) - 1:
		#sig_row_start += (info[i][1][0] * v1[0] + info[i][1][1] * v2[0])
		eps_row_start += v1[1]

# Read the parameters in, passed as arguments.
# There are 46 keys, and 11 rows in each grid. Parallelizing each row gives 506 jobs.
# There are a total of 7,590 points to be determined.
SGE_TASK_ID = int(sys.argv[1])
k_max = int(sys.argv[2])
l_max = int(sys.argv[3])
m_max = int(sys.argv[4])
n_max = int(sys.argv[5])
row_index = int(sys.argv[6])
precision = int(sys.argv[7])
tolerance = float(sys.argv[8])

key = [k_max, l_max, m_max, n_max]

mixed = MixedCorrelator()

bootstrap.prec = precision
bootstrap.chol_tol = tolerance

mixed.point_file = SGE_TASK_ID.__str__()

mixed.determine_points(key, row_lists[row_index])
=======
version https://git-lfs.github.com/spec/v1
oid sha256:57028a635cd97e6cf17c77bdf0aa3d2c99046b31bb57fd9b916f9dcd9ac74a9c
size 1802
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
