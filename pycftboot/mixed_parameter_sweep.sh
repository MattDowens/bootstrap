#!/bin/bash

# SGE Options
#$ -N mixed_parameter_sweep
#$ -j y
#$ -V # use all shell environment variables
#$ -l h_rt=168:00:00
# This is to speficy queue preference.
# #$ -q sopa.1.day

# Request 16 cores.
#$ -pe omp 16

# Create Working Directory
WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$SGE_TASK_ID"
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
cp "$HOME"/bootstrap/mixed_keys.txt "$WDIR"

# This will eventually use sed to edit a parameter file, a long list of
# inputs depending on $SGE_TASK_ID.
python mixed_parameter_sweep.py $SGE_TASK_ID $(head -n $SGE_TASK_ID mixed_keys.txt | tail -1)

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$SGE_TASK_ID".py $RDIR

# Cleanup
rm -rf $WDIR
