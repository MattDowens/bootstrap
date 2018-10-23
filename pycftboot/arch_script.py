<<<<<<< HEAD
import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from archipelago import *
import sys

SGE_TASK_ID = int(sys.argv[1])
row_index = SGE_TASK_ID - 1
# Generate grid of points and row_lists, to index in determine_points
phi_step = 0.001
sing_step = 0.05

# Don't start either dimension exactly on the unitarity bound. This will cause problems.
start = [0.505, 1.05]
stop = [0.53, 2.0]

key = [20, 20, 2, 4]

mixed = MixedCorrelator(N = 1)
mixed.point_file = SGE_TASK_ID.__str__()
rows = mixed.generate_rows(start, stop, phi_step, sing_step)
bootstrap.prec = 800
mixed.determine_row(key, rows[row_index])
=======
version https://git-lfs.github.com/spec/v1
oid sha256:fec867d1611f7055f539987a100416a64e4e4eb82debd2b4fa99040674de415e
size 699
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
