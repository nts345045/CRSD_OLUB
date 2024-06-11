#!/bin/bash
#
# This script runs everything necessary to reproduce results presented
# in Stevens et al. (202X) from minimally processed data sources archived
# in their data repository.
ENVNAME='crsd'
# Check if the environment is active
if [[ "$CONDA_DEFAULT_ENV" == "$ENVNAME" ]]; then
    echo "Environment '$ENVNAME' already active"
# If not active, but exists, activate
elif conda info --envs | grep -q "$ENVNAME"
    echo "Activating '$ENVNAME'"
    conda activate "$ENVNAME"
# Otherwise 
else
    echo "Environment '$ENVNAME' does not exist - exiting"
    exit
fi

# Pressure Transducers Initial Processing
STRESS_RAW_FILE='../data/0_raw/Timeseries/RS_RAWdata_OSC_N.mat'
STRESS_PUTC_FILE='../data/1_preprocessed/Timeseries/PhysicalUnitsData__UTC_Timing.csv'
python ../processing/initial/CRSD_volts2phys.py -i $STRESS_RAW_FILE -o $STRESS_PUTC_FILE

# LVDT Initial Processing
LVDT_RAW_FILES='../data/0_raw/Timeseries/LVDT/*.txt'
LVDT_UTC_FILE='../data/1_preprocessed/Timeseries/Stitched_LVDT_Data__UTC_Timing.csv'
python ../processing/initial/merge_raw_LVDT.py -i $LVDT_RAW_FILES -o $LVDT_UTC_FILE -t 0.05 -r 1


echo "Will run processing scripts here"
echo "Will run figure rendering scripts here"