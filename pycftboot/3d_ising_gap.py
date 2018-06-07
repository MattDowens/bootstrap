import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np

#Start timing
start_time=time.time()
start_cpu=time.clock()

#Parameters for SDPB
bootstrap.cutoff=1e-10
dim=3
k_max=20
l_max=15
n_max=4
m_max=2

#Initializing conformal and convolved conformal blocks
tab1=bootstrap.ConformalBlockTable(dim,k_max,l_max,m_max,n_max)
tab2=bootstrap.ConvolvedBlockTable(tab1)

#Plots all allowed points in a coarse grid

sig=np.arange(0.5,0.85,0.05)
eps=np.arange(1.0,2.2,0.2)









#Computing and formatting times (Can shorten this!)
end_time=time.time()
end_cpu=time.clock()
run_time=end_time-start_time
cpu_time=end_cpu-start_cpu
run_time1=time.gmtime(run_time)
run_time2=time.strftime("%H:%M:%S",run_time1)
cpu_time1=time.gmtime(cpu_time)
cpu_time2=time.strftime("%H:%M:%S",cpu_time1)
print("Run time "+run_time2, "CPU time "+cpu_time2)