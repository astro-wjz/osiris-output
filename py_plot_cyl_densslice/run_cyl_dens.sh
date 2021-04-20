#! /bin/bash

######## Description ########
# Program for visualizing hdf5 result files from Osiris cyl modes code.

######## How to use #########
# Two input parameters in file "run_cyl_ori.sh"
# Users should modify them before running
# workpath: path to folder "FLD", which contains original h5 files
# phi: angle of the slice along z axis

######## Results #########
# PNG files will be output to folder "RESULTS" which has same level with "FLD"

workpath="/Users/astrowjz/Desktop/read_h5/trans2silo/DENSITY"
phi=0.0
rmax=60.0
zmin=-10.0
zmax=50.0
npr=400
npz=3840

python3 plot_cyl_dens.py ${workpath} ${phi} ${rmax} ${zmin} ${zmax} ${npr} ${npz}

echo " "
echo The figures are stored into path: '"'${workpath/FLD/RESULTS}'"'.
