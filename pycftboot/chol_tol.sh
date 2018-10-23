#!/bin/bash

# SGE Options
#$ -N chol_tol
#$ -j n
#$ -V # use all shell environment variables
#$ -l h_rt=168:00:00
# This is to speficy queue preference.
# #$ -q sopa.1.day

# Request 16 cores.
#$ -pe omp 16

#$ -m e
#$ -M mtd5@st-andrews.ac.uk

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
cp "$HOME"/bootstrap/tab_0_0 "$WDIR"
cp "$HOME"/bootstrap/tab_-0.894_-0.894 "$WDIR"
cp "$HOME"/bootstrap/tab_0.894_-0.894 "$WDIR"

# This will eventually use sed to edit a parameter file, a long list of
# inputs depending on $SGE_TASK_ID.
python chol_tol.py

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "[60, 50, 5, 7]".py $RDIR

# Cleanup
# rm -rf $WDIR
