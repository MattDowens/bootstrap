<<<<<<< HEAD
import re

with open("mixed_param_sweep.py", "a") as new:
	with open("cat_file.py", 'r') as old:
		for line in old:
			new_line = re.sub("(\d+:\d+:\d+)", 'time.strptime("\\1", "%H:%M:%S")', line)
			new.write(new_line)
=======
version https://git-lfs.github.com/spec/v1
oid sha256:e4cf35626c0b629bc824a35b8c2189fbfd5c2ab14083fbe2307a81fc9ff6648d
size 218
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
