# Python program to generate parameter file.
# We choose a job instance to iterate through all (m, n) for a given (k, l), so we have 400 jobs.
# N.b this is a necessary choice to keep each job self-contained to allow embarassing parallelization.

# In this case, k_start = k_stop and l_start = l_stop always.
# Also, m_start = n_start = 1 and m_stop = n_stop = 20 always.

# Must have line number = $SGE_TASK_ID.

name = "parameters"

SGE_TASK_ID = 1

k_start = 1
k_stop = 20
l_start = 1
l_stop = 20

m_start = 1
m_stop = 20
n_start = 1
n_stop = 20

# Write .txt file in form k_st, k_sp, l_st, l_sp, m_st, m_sp, n_st, n_sp for each job.
with open(name + ".txt", 'w') as file:
	while k_start <= k_stop:
		while l_start <= l_stop:
			file.write(str(k_start) + " " + str(k_start) + " " + 
				str(l_start) + " " + str(l_start) + " " + str(m_start) + " " + str(m_stop) +
				" " + str(n_start) + " " + str(n_stop) + "\n")
			l_start += 1
			if l_start == l_stop +1:
				break
#			SGE_TASK_ID += 1
		k_start += 1
		l_start = 1
#		SGE_TASK_ID += 1