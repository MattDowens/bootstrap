#!/bin/bash

# SGE Options
#$ -N mixed_island
#$ -j y
#$ -V # use all shell environment variables
#$ -l h_rt=24:00:00
# This is to speficy queue preference.
#$ -q sopa.1.day

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

# This will eventually use sed to edit a parameter file, a long list of
# inputs depending on $SGE_TASK_ID.
python mixed_correlator_job.py $SGE_TASK_ID

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

ROW_INDEX=$(($SGE_TASK_ID-1))
# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$ROW_INDEX".py $RDIR

# Cleanup
rm -rf $WDIR
