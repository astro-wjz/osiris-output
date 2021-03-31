#! /bin/bash

######## Description ########
# Program for vasualizing hdf5 result files from Osiris cyl modes code.

######## How to use #########
# Two input parameters in file "run_cyl_ori.sh"
# Users should modify them before running
# workpath: path to folder "FLD", which contains original h5 files
# phi: angle of the slice along z axis

######## Results #########
# PNG files will be output to folder "RESULTS" which has same level with "FLD"

workpath="/Users/astrowjz/Desktop/read_h5/trans2silo/FLD"
phi=0.0

python3 plot_cyl_ori.py ${workpath} ${phi}

echo " "
echo The figures are stored into path: '"'${workpath/FLD/RESULTS}'"'.
