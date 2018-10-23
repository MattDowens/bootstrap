#!/bin/sh

#$ -N jobname # job name

#$ -V # use all shell environment variables

#$ -cwd # run job in working directory

#$ -j y # merge stdout and stderr to one file

 

# Choose a queue:

# Check options with "qconf -sql"

# Check details with "qconf -sq ≺q-name≻"

#$ -q cdt.7.day

 

# Choose a parallel environment:

# Check options with "qconf -spl"

# Check details with "qconf -sp ≺pe-name≻"

#$ -pe mpi16

 

# Send mail at submission and completion of script#

# #$ -m be

# #$ -M email@provider

 

# Set job runtime

#$ -l h_rt=24:00:00

 

echo "Hello World"

 

date

sleep 60

date