<<<<<<< HEAD
import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import subprocess
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages
from new_ising_class import *

print(os.getpid())
row_lists = [[[0.518],[1.397]]]
row = row_lists[0]
key = [10, 10, 1, 3]
bootstrap.prec = 500
bootstrap.cutoff=0
reference_sdp = None
for i in range(len(row[0])):
    sig = row[0][i]
    eps = row[1][i]

    global start_time
    start_time = time.time()
    global start_cpu
    start_cpu = time.clock()
    g_tab1 = bootstrap.ConformalBlockTable(3, *key)
    g_tab2 = bootstrap.ConformalBlockTable(3, *(key + [eps-sig, sig-eps, "odd_spins = True"]))
    g_tab3 = bootstrap.ConformalBlockTable(3, *(key + [sig-eps, sig-eps, "odd_spins = True"]))
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
    point.save("a_test_point")
=======
version https://git-lfs.github.com/spec/v1
oid sha256:4a5aafd58e48fbe88155055413a059c125727d8d20915bcc3fc67fabf1550e6b
size 4227
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
