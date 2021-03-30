#! /bin/bash

# INPUT INFORMATION
codepath="/public3/home/sc52879/astrowjz/osiris/astrowjz/trans2silo/plotsilo2d"
workpath="/public3/home/sc52879/astrowjz/osiris/astrowjz/cyl01/MS/FLD"  # PATH TO /FLD/
folders=("bf" "ef")
n_row=160   # cell number of r direction
n_col=320   # cell number of z direction
phi0=0.00   # slice to be drawn
zmin=0.00
zmax=200.00
rmax=100.00
txt_switch="off" # "off" or "on"   # if need transfer hdf5 to txt files

# TRANSFER HDF5 FILES TO TXT FILES
if [ $txt_switch = "on" ]
then
    echo "TRANSFER HDF5 FILES TO TXT FILES ... "
    cd ${workpath}
    n=(`ls MODE-0-RE/b1_cyl_m/ | wc -l`)
    mkdir b1_re_0 b1_re_1 b1_im_1 b2_re_0 b2_re_1 b2_im_1 \
          b3_re_0 b3_re_1 b3_im_1 e1_re_0 e1_re_1 e1_im_1 \
          e2_re_0 e2_re_1 e2_im_1 e3_re_0 e3_re_1 e3_im_1
    cd ${codepath}
    module load python/3.7.6-public3
    python read_h5.py $n ${workpath}
    module unload python/3.7.6-public3
fi

# TRANSFER TXT FILES TO SILO FILES
echo "============================="
make clean
make
echo "============================="
echo "TRANSFER TXT FILES TO SILO FILES ... "

cd ${workpath}
n=(`ls MODE-0-RE/b1_cyl_m/ | wc -l`)
mkdir bf ef
f_re0=("b1_re_0" "e1_re_0")
f_re1=("b1_re_1" "e1_re_1")
f_im1=("b1_im_1" "e1_im_1")
for nfolder in {1..2}
do
    cd ${workpath}
    list1=(`ls ${f_re0[$nfolder-1]}`)
    list2=(`ls ${f_re1[$nfolder-1]}`)
    list3=(`ls ${f_im1[$nfolder-1]}`)
    cd ${codepath}
    for((i=1;i<=$n;i++))
    do
        ./test.e ${n_row} ${n_col} ${phi0} ${workpath} ${folders[$nfolder-1]} ${list1[$i-1]} ${list2[$i-1]} ${list3[$i-1]} ${rmax} ${zmin} ${zmax}
        echo " $i of $n files in ${folders[$nfolder-1]} output successfully !"
    done
done
make clean
echo "=================Finished!=================="
