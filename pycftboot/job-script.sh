#!/bin/bash

# SGE Options
#$ -N test_job
#$ -j y
#$ -V # use all shell environment variables

# Create Working Directory
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
python job_script.py $SGE_TASK_ID $(head -n $SGE_TASK_ID parameters.txt | tail -1)

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$SGE_TASK_ID".py $RDIR

# Cleanup
rm -rf $WDIR
