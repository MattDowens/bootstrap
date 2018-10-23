#!/bin/bash

# SGE Options
#$ -cwd # run job in working directory
#$ -N plots
#$ -j y
#$ -V # use all shell environment variables
#$ -l h_rt=168:00:00

python plot_script.py