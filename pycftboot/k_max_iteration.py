import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np

#Start timing
start_time=time.time()
start_cpu=time.clock()
"""
Parameters for SDPB 
bootstrap.cutoff=1e-10
dim=3
k_max=20
l_max=15
n_max=4
m_max=2
"""

#Plots all allowed points in a coarse grid
def plot_grid(dim,table,sig_range,eps_range):
    allowed_sig=[]
    allowed_eps=[]
    disallowed_sig=[]
    disallowed_eps=[]
    for sig in sig_range:
        for eps in eps_range:
            sdp=bootstrap.SDP(sig,table)
            sdp.set_bound(0,float(dim))
            sdp.add_point(0,eps)
            result=sdp.iterate()
            if result:
                allowed_sig.append(sig)
                allowed_eps.append(eps)
            else:
                disallowed_sig.append(sig)
                disallowed_eps.append(eps)
    plt.plot(allowed_sig,allowed_eps,'r+')
    plt.plot(disallowed_sig,disallowed_eps,'b+')
    plt.show()

#Iterates through k_max and plots a grid for each value, keeping values of all other parameters constant.
def iterate_k_max(k_range):
    bootstrap.cutoff=1e-10
    dim=3
    l_max=15
    n_max=4
    m_max=2
    for k in k_range:
        tab1=bootstrap.ConformalBlockTable(dim,k_max,l_max,m_max,n_max)
        tab2=bootstrap.ConvolvedBlockTable(tab1)
        plot_grid(dim,tab2,sig_set,eps_set)

#Example
k_set=np.arange(1,21,1)
sig_set=np.arange(0.5,0.85,0.05)
eps_set=np.arange(1.0,2.2,0.2)
iterate_k_max(k_set)

#Example
plot_grid(dim,tab2,sig_set,eps_set)

#Computing and formatting times
end_time=time.time()
end_cpu=time.clock()
run_time=time.strftime("%H:%M:%S",time.gmtime(end_time-start_time))
cpu_time=time.strftime("%H:%M:%S",time.gmtime(end_cpu-start_cpu))
print("Run time "+run_time, "CPU time "+cpu_time)