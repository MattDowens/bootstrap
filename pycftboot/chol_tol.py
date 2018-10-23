import bootstrap
import subprocess
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from new_ising_class import *
import math
import mpmath

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

key = [60, 50, 5, 7]
row_index = 4
mixed = MixedCorrelator()
bootstrap.prec = 2000
mixed.point_file = key.__str__()

bootstrap.chol_tol = 1e-300

reference_sdp = None
for i in range(len(row_lists[row_index])):
    sig = row_lists[row_index][0][i]
    eps = row_lists[row_index][1][i]

    global start_time
    start_time = time.time()
    global start_cpu
    start_cpu = time.clock()
    g_tab1 = bootstrap.ConformalBlockTable(0, 0, 0, 0, 0, name = "tab_0_0")
    g_tab2 = bootstrap.ConformalBlockTable(0, 0, 0, 0, 0, name = "tab_0.894_-0.894")
    g_tab3 = bootstrap.ConformalBlockTable(0, 0, 0, 0, 0, name = "tab_-0.894_-0.894")
    f_tab1a = bootstrap.ConvolvedBlockTable(g_tab1)
    f_tab1s = bootstrap.ConvolvedBlockTable(g_tab1, symmetric = True)
    f_tab2a = bootstrap.ConvolvedBlockTable(g_tab2)
    f_tab2s = bootstrap.ConvolvedBlockTable(g_tab2, symmetric = True)
    f_tab3 = bootstrap.ConvolvedBlockTable(g_tab3)
    tab_list = [f_tab1a, f_tab1s, f_tab2a, f_tab2s, f_tab3]
    global now
    global now_clock
    global CB_time
    global CB_cpu
    now = time.time()
    now_clock = time.clock()
    CB_time = datetime.timedelta(seconds = int(now - start_time))
    CB_cpu = datetime.timedelta(seconds = int(now_clock - start_cpu))
    print("The calculation of the required conformal blocks has successfully completed.")
    print("Time taken: " + str(CB_time))
    print("CPU_time: " + str(CB_cpu))
    vec3 = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 4, 1, 0], [-1, 2, 0, 0], [1, 3, 0, 0]]
    vec2 = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 4, 1, 0], [1, 2, 0, 0], [-1, 3, 0, 0]]
    m1 = [[[1, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0]]]
    m2 = [[[0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [1, 0, 1, 1]]]
    m3 = [[[0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0]]]
    m4 = [[[0, 0, 0, 0], [0.5, 0, 0, 1]], [[0.5, 0, 0, 1], [0, 0, 0, 0]]]
    m5 = [[[0, 1, 0, 0], [0.5, 1, 0, 1]], [[0.5, 1, 0, 1], [0, 1, 0, 0]]]
    vec1 = [m1, m2, m3, m4, m5]
    info = [[vec1, 0, "z2-even-l-even"], [vec2, 0, "z2-odd-l-even"], [vec3, 1, "z2-odd-l-odd"]]
    
    if reference_sdp == None:
        sdp = bootstrap.SDP([sig, eps], tab_list, vector_types = info)
        reference_sdp = sdp
    else:
        sdp = bootstrap.SDP([sig, eps], tab_list, vector_types = info, prototype = reference_sdp)
    sdp.set_bound([0, "z2-even-l-even"], 3)
    sdp.set_bound([0, "z2-odd-l-even"], 3)
    sdp.add_point([0, "z2-even-l-even"], eps)
    sdp.add_point([0, "z2-odd-l-even"], sig)
    sdp.set_option("maxThreads", 16)
    sdp.set_option("dualErrorThreshold", 1e-15)

    print("Testing point " + "(" + sig.__str__() + ", " + eps.__str__() +")...")
    
    name = "test_SDP"
    obj = [0.0] * len(sdp.table[0][0][0].vector)
    sdp.write_xml(obj, sdp.unit, name)
    print(os.getpid())
    sdpb = subprocess.Popen(["sdpb", "-s", name + ".xml", "--precision=" + str(bootstrap.prec), "--findPrimalFeasible", "--findDualFeasible", "--noFinalCheckpoint"] + sdp.options)
    print(str(os.getppid()))
    print("Running SDPB. Process ID: " + str(sdpb.pid))
    sdpb.wait()
    print("SDPB has finished running. RETURN code: " + str(sdpb.returncode))
    output = sdp.read_output(name = name)
    terminate_reason = output["terminateReason"]  
    result = terminate_reason == "found primal feasible solution"

    end_time = time.time()
    end_cpu = time.clock()
    global sdp_time
    global sdp_cpu
    sdp_time = datetime.timedelta(seconds = int(end_time - bootstrap.now2))
    sdp_cpu = datetime.timedelta(seconds = int(end_cpu - bootstrap.now2_clock))
    run_time = datetime.timedelta(seconds = int(end_time - start_time))
    cpu_time = datetime.timedelta(seconds = int(end_cpu - start_cpu))

    print("The SDP has finished running.")
    print("Time taken: " + str(sdp_time))
    print("CPU_time: " + str(sdp_cpu))
    print("See point file for more information. Check the times are consistent")

    point = Point(*([sig, eps] + key + [result, run_time, cpu_time, CB_time, CB_cpu, bootstrap.xml_time, bootstrap.xml_cpu, sdp_time, sdp_cpu]))
    point.save(mixed.point_file)