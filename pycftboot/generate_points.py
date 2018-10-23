sig_step = 0.0001/13
eps_step = 0.001/13

v1 = [0, eps_step]
v2 = [sig_step, sig_step]

start = [0.51799, 1.411]
info = [[3, [1,1]], [4, [1,1]], [5, [0,1]], [7, [1,1]], [7, [1,1]], [8, [1,1]], [9, [1,1]], [10, [1,1]], [11, [1,1]], [11, [0,1]], [13, [1,1]], [14, [1,1]], [14, [1,1]], [15, [1,1]], [15, [1,1]], [16, [1,1]], [16, [1,1]], [17, [1,1]], [17, [1,1]], [18, [1,1]], [18, [1,1]], [18, [1,2]], [18, [1,1]], [18, [1,1]], [18, [1,1]], [19, [1,2]], [18, [1,1]], [18, [1,1]], [19, [1,1]], [19, [1,2]], [18, [1,1]], [19, [1,1]], [19, [1,2]], [18, [1,1]], [18, [1,1]], [19, [1,2]], [18, [1,1]], [18, [1,2]], [17, [1,1]], [17, [1,2]], [17, [1,2]], [16, [1,2]], [15, [1,2]], [14, [1,2]], [13, [1,2]], [12, [0,0]]]

sig_start = start[0]
eps_start = start[1]

sig_values = []
eps_values = []

row_lists = []
sig_row_start = sig_start
eps_row_start = eps_start
sigs = []
eps = []
for i in range(len(info)):
	row_lists.append([])
	for points in range(info[i][0] + 1):
		sigs.append(sig_row_start + points*v2[0])
		eps.append(eps_row_start + points*v2[1])
		sig_values.append(sig_row_start + points*v2[0])
		eps_values.append(eps_row_start + points*v2[1])
	row_lists[i].append(sigs)
	row_lists[i].append(eps)
	sigs = []
	eps = []
	# Alter the starting position of the next row.
	if i!= len(info) -1:
		sig_row_start += (info[i][1][0] * v1[0] + info[i][1][1] * v2[0])
		eps_row_start += (info[i][1][0] * v1[1] + info[i][1][1] * v2[1])
