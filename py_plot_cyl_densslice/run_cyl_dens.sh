#! /bin/bash

######## Description ########
# Program for vasualizing hdf5 result files from Osiris cyl modes decomposition code, 
# and combine a slice along z-driction at any angle. Especially for plotting density files.

######## How to use #########
# Seven input parameters in file "run_cyl_dens.sh"
# Users should modify them before running
# workpath: path to folder "DENSITY", which contains original h5 files
# phi: angle of the slice along z axis
# rmax: the real max length of r direction
# zmin: the real min position of z direction
# zmax: the real max position of z direction
# npr: total amount of points along r direciton
# npz: total amount of points along z direction

######## Results #########
# Images and movies will be output to folder "RESULTS" which has same level with "DNESITY"

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
