import bootstrap
import matplotlib.pyplot as plt
import time
import datetime

start_time=time.time()
start_cpu=time.clock()
bootstrap.cutoff=1e-10
dim=3
k_max=20
l_max=15
n_max=4
m_max=3
sig=0.52
eps=1.2

table1=bootstrap.ConformalBlockTable(dim,k_max,l_max,m_max,n_max)
table2=bootstrap.ConvolvedBlockTable(table1)

sdp=bootstrap.SDP(sig,table2)
sdp.set_bound(0,3.0)
sdp.add_point(0,eps)
result=sdp.iterate()

end_time=time.time()
end_cpu=time.clock()
run_time=end_time-start_time
cpu_time=end_cpu-start_cpu
run_time1=time.gmtime(run_time)
run_time2=time.strftime("%H:%M:%S",run_time1)
cpu_time1=time.gmtime(cpu_time)
cpu_time2=time.strftime("%H:%M:%S",cpu_time1)
print("Run time "+run_time2, "CPU time "+cpu_time2)
print(result)

