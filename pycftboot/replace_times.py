import re

with open("mixed_param_sweep.py", "a") as new:
	with open("cat_file.py", 'r') as old:
		for line in old:
			new_line = re.sub("(\d+:\d+:\d+)", 'time.strptime("\\1", "%H:%M:%S")', line)
			new.write(new_line)