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