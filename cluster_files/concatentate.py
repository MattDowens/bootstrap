# Put this file in the working directory of the master 'Results' folder.
# It will iterate through python files, and concatentat them into one file.

import os

basepath = os.getcwd()
for filename in os.listdir(basepath):
    if filename.endswith(".py") and filename != "cat_file.py" and filename != "concatentate.py": 
        with open(basepath + "/" + filename, 'r') as openfile:    
            with open("cat_file.py", 'a') as cat_file:
            	for line in openfile:
            		cat_file.write(line)
