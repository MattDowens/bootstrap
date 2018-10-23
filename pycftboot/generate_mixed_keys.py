import math

def compute_n(kmax):
	return math.floor(kmax**(0.5))

with open("mixed_keys" + ".txt", 'w') as file:
	for i in range(15, 61):
		for j in range(0, 11, 1):
			if i<50:
				file.write(str(i) + " " + str(i) + " " + str(compute_n(i)-2) + " " + str(compute_n(i)) + " " + str(j) + "\n")
			else:
				file.write(str(i) + " " + str(50) + " " + str(compute_n(i)-2) + " " + str(compute_n(i)) + " " + str(j) + "\n")