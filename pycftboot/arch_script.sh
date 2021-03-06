#!/bin/bash

# SGE Options
#$ -N O(1)
#$ -j n
#$ -V # use all shell environment variables
#$ -cwd
#$ -l h_rt=168:00:00
# This is to speficy queue preference.
#$ -q cdt.7.day

# Request 16 cores.
#$ -pe omp 16

# #$ -m e
# #$ -M mtd5@st-andrews.ac.uk

# Create Working Directory
#WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"
WDIR=/scratch/"$USER"/"$JOB_NAME"-"$SGE_TASK_ID"
mkdir -p $WDIR
if [ ! -d $WDIR ]
then
  echo $WDIR not created
  exit
fi
cd $WDIR

# Copy Data and Config Files.
# Don't need SDPB in the working directory. SDPB has been hard-coded to PyCFTBoot files (in common.py).
cp "$HOME"/bootstrap/*.py "$WDIR"

# This will eventually use sed to edit a parameter file, a long list of
# inputs depending on $SGE_TASK_ID.
python arch_script.py $SGE_TASK_ID

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$SGE_TASK_ID".py $RDIR

# Cleanup
rm -rf $WDIR