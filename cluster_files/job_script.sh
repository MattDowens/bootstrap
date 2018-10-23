#!/bin/bash

# SGE Options
#$ -N ising_gap
#$ -j y
#$ -V # use all shell environment variables
#$ -l h_rt=168:00:00

# Request one day for l<=10 and 7 days for l>10.
# Can probably get away with l>12 instead.
#if [ $(($SGE_TASK_ID%20)) -ge 10 ]
#then
#	#$ -l h_rt=168:00:00
#else
#	#$ -l h_rt=24:00:00
#fi

# Mail me notifications, beginning, ending, and abortion.
# #$ -m bea
# #$ -M mtd5@st-andrews.ac.uk

# This is to speficy queue preference.
# #$ -q cm.7.day

# Padded SGE_TASK_ID. This will also be the name of the save file.
# SGE_ID = printf "%03d" $SGE_TASK_ID

# Create Working Directory
# WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"-"$SGE_TASK_ID"
WDIR="$HOME"/bootstrap/"$JOB_NAME"-"$JOB_ID"-"$SGE_TASK_ID"
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
python job_script.py $SGE_TASK_ID $(head -n $SGE_TASK_ID parameters.txt | tail -n -1)

echo "Running on $(hostname)"
echo "We are in $(pwd)"
date

# Copy Results Back to Home Directory
RDIR="$HOME"/bootstrap/Results/"$JOB_NAME"-"$JOB_ID"
mkdir -p $RDIR
cp "$SGE_TASK_ID".py "$RDIR"

# Cleanup
rm -rf $WDIR
