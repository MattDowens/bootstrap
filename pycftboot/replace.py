with open("new_master.py", 'r') as old_file:
	with open("master.py", "a") as new_file:
		for line in old_file:
			new_file.write(line.replace("datetime", "time"))