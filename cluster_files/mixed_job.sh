#!/bin/bash

# SGE Options
#$ -N mixed_test
#$ -j y
#$ -V # use all shell environment variables
#$ -l h_rt=24:00:00
# This is to speficy queue preference.
#$ -q sopa.1.day

# Request 16 cores.
#$ -pe omp 16

# Create Working Directory
# WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"-"$SGE_TASK_ID"
WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"
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
cp "$HOME"/bootstrap/parameters.txt "$WDIR"

# This will eventually use sed to edit a parameter file, a long list of
# inputs depending on $SGE_TASK_ID.
python mixed_job.py

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "mixed_test".py "$RDIR"

# Cleanup
rm -rf $WDIR