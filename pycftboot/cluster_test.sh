#!/bin/sh

#$ -N cluster_test # job name

#$ -V # use all shell environment variables

#$ -cwd # run job in working directory

#$ -j y # merge stdout and stderr to one file

 

# Choose a queue:

# Check options with "qconf -sql"

# Check details with "qconf -sq ≺q-name≻"

#$ -q cdt.7.day
 

# Set job runtime

#$ -l h_rt=24:00:00

python cluster_test.py