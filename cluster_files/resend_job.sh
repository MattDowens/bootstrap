#!/bin/bash

# SGE Options
#$ -N test_job
#$ -j y
#$ -V # use all shell environment variables

# We want to input the $SGE_TASK_ID of the failed job as an argument to the resend_job.sh.
# Create Working Directory
WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"-"$1"
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
# inputs depending on the argument passed in the command-line.
python job_script.py $1 $(head -n $1 parameters.txt | tail -n -1)

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$1.py" "$RDIR"

# Cleanup
rm -rf $WDIR
