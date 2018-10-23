<<<<<<< HEAD
import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from archipelago import *
import sys
#bootstrap.sdpb_path = "/usr/local/Cellar/sdpb/0.0.2/bin/sdpb"
SGE_TASK_ID = int(sys.argv[1])
index = SGE_TASK_ID - 1

phi_num = 30
sing_num = 20

start = [0.501, 1.05]
stop = [0.53, 2.0]

mixed = MixedCorrelator(N = 1)
mixed.point_file = SGE_TASK_ID.__str__()
rows = mixed.generate_rows(start, stop, phi_num, sing_num)
bootstrap.prec = 800

#phi = eval_mpfr(rows[11][0][10], bootstrap.prec)
#sing = eval_mpfr(rows[11][1][10], bootstrap.prec)
phi1 = eval_mpfr(rows[4][0][1], bootstrap.prec)
sing1 = eval_mpfr(rows[4][1][1], bootstrap.prec)
phi2 = eval_mpfr(rows[4][0][17], bootstrap.prec)
sing2 = eval_mpfr(rows[4][1][17], bootstrap.prec)
phi_list = [phi1, phi2]
sing_list = [sing1, sing2]

k_range = np.arange(40, 61, 1).tolist()
l_range = np.arange(40, 61, 1).tolist()

keys = []
for k in k_range:
    for l in l_range:
        keys.append([k, l, 5, 7])

# for n in np.arange(2,16,1):
#key = [n**2, n**2, n-2, n]
key = keys[index]
print("Computing conformal blocks for k=" + key[0].__str__() + ", l=" + key[1].__str__() + ", m=5, n=7.")
start = time.time()
start_cpu = time.clock()
g_tab1 = bootstrap.ConformalBlockTable(3, *(key + [0, 0, "odd_spins = True"]))
g_tab2 = bootstrap.ConformalBlockTable(3, *(key + [phi1 - sing1, phi1 - sing1, "odd_spins = True"]))
g_tab3 = bootstrap.ConformalBlockTable(3, *(key + [sing1 - phi1, phi1 - sing1, "odd_spins = True"]))

f_tab1a = bootstrap.ConvolvedBlockTable(g_tab1)
f_tab1s = bootstrap.ConvolvedBlockTable(g_tab1, symmetric = True)
f_tab2a = bootstrap.ConvolvedBlockTable(g_tab2)
f_tab3a = bootstrap.ConvolvedBlockTable(g_tab3)
f_tab3s = bootstrap.ConvolvedBlockTable(g_tab3, symmetric = True)

tab_list = [f_tab1a, f_tab1s, f_tab2a, f_tab3a, f_tab3s]

for tab in [g_tab1, g_tab2, g_tab3]:
# tab.dump("tab_" + str(tab.delta_12) + "_" + str(tab.delta_34))
	del tab
    
dimension = (5 * len(f_tab1a.table[0].vector)) + (2 * len(f_tab1s.table[0].vector))
max_dimension = 0
for tab in tab_list:
    max_dimension = max(max_dimension, len(tab.table[0].vector))

print("Number of components (dim of PolynomialVectorMatrices) : " + dimension.__str__() + ".")
print("Kmax should be around (max dimension of convolved block tables): " + max_dimension.__str__() + ".")
print("It is: " + key[0].__str__() + ".")
cb_end = time.time()
cb_end_cpu = time.clock()
cb_time = datetime.timedelta(seconds = int(cb_end - start))
cb_cpu = datetime.timedelta(seconds = int(cb_end_cpu - start_cpu))
print("The calculation of the required conformal blocks has successfully completed.")
print("Time taken: " + str(cb_time))
print("CPU_time: " + str(cb_cpu))
    
#print("Creating SDP and writing XML file.")

for i in [0, 1]:
	phi = phi_list[i]
	sing = sing_list[i]
	print("Creating SDP and writing XML file for phi=" + phi.__str__() + " and sing=" + sing.__str__() + ".")
	sdp = bootstrap.SDP([phi, sing], tab_list, vector_types = mixed.info)
    
	# We assume the continuum in both even vector and even singlet sectors begins at the dimension=3.
	sdp.set_bound([0, 0], 3)
	sdp.set_bound([0, 3], 3)

	# Except for the two lowest dimension scalar operators in each sector.
	sdp.add_point([0, 0], sing)
	sdp.add_point([0, 3], phi)

	sdp.set_option("maxThreads", 16)
	sdp.set_option("dualErrorThreshold", 1e-15)
	sdp.set_option("maxIterations", 1000)

	# Run the SDP to determine if the current operator spectrum is permissable.
	print("Testing point " + "(" + phi.__str__() + ", " + sing.__str__() + ") " + "with " + dimension.__str__() + " components.")
    
	name = "test_SDP"
	obj = [0.0] * len(sdp.table[0][0][0].vector)
	sdp.write_xml(obj, sdp.unit, name)

	xml_end = time.time()
	xml_end_cpu = time.clock()
	xml_time = datetime.timedelta(seconds = int(xml_end - cb_end))
	xml_cpu = datetime.timedelta(seconds = int(xml_end_cpu - cb_end_cpu))
    
	sdpb = subprocess.Popen([bootstrap.sdpb_path, "-s", name + ".xml", "--precision=" + str(bootstrap.prec), "--findPrimalFeasible", "--findDualFeasible", "--noFinalCheckpoint"] + sdp.options)
	print(str(os.getppid()))
	print("Running SDPB. Process ID: " + str(sdpb.pid))
	sdpb.wait()
	print("SDPB has finished running. RETURN code: " + str(sdpb.returncode))

	end = time.time()
	end_cpu = time.clock()
	sdp_time = datetime.timedelta(seconds = int(end - xml_end))
	sdp_cpu = datetime.timedelta(seconds = int(end_cpu - xml_end_cpu))
	run_time = datetime.timedelta(seconds = int(end - start))
	cpu_time = datetime.timedelta(seconds = int(end_cpu - start_cpu))
    
	if sdpb.returncode != 0:
    	print("There was a problem running SDPB. See the process returncode attribute for more info.")
#   	continue
        
	output = sdp.read_output(name = name)
	terminate_reason = output["terminateReason"]
	result = terminate_reason == "found primal feasible solution"
	print("The result is: " + result.__str__())
	if result == True:
 		print("The point " + "(" + float(phi).__str__() + "," + float(sing).__str__() + ") " + " is ALLOWED for " + dimension.__str__() + " components.")
	if result == False:
  		print("The point " + "(" + float(phi).__str__() + "," + float(sing).__str__() + ") " + " is DISALLOWED for " + dimension.__str__() + " components.")

	point = Point(*([phi, sing] + key + [dimension, max_dimension, result, run_time, cpu_time, cb_time, cb_cpu, xml_time, xml_cpu, sdp_time, sdp_cpu]))
	point.save(mixed.point_file)
=======
version https://git-lfs.github.com/spec/v1
oid sha256:5aaba2f304e5d669d974a1e538dbd364f09d54a657f9db6e46f705957d041b98
size 5485
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
