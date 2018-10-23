# This is the script for one job instance, parametrized by $SGE_TASK_ID.
import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from revised_ising_class import *
import sys

mixed = MixedCorrelator("mixed_test")

mixed.sig_step = 0.0001
mixed.eps_step = 0.001

mixed.determine_points([20, 20, 12, 12])