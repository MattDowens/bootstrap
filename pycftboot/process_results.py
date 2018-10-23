<<<<<<< HEAD
# Put this file in the working directory of the master 'Results' folder.
# It will iterate through python files, and concatentat them into one file.

import os
import re

basepath = os.getcwd()
for filename in os.listdir(basepath):
    if filename.endswith(".py") and filename != "cat_file.py" and filename != "concatentate.py": 
        with open(basepath + "/" + filename, 'r') as openfile:    
            with open("cat_file.py", 'a') as cat_file:
            	for line in openfile:
            		new_line = re.sub("(\d+:\d+:\d+)", 'time.strptime("\\1", "%H:%M:%S")', line)
            		cat_file.write(line)
=======
version https://git-lfs.github.com/spec/v1
oid sha256:ee40a361a69a51ecd9bd02a87bd87c94430d9bc55ea19787fba6c3456030212c
size 612
>>>>>>> d87b7d1ea1656ad601911b3142003880ece5c013
