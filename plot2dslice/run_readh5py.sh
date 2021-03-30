#! /bin/bash

######## Description ########
# Program for formatting Osiris 2D hdf5 files to txt data files.
# Program for plotting Osiris 2D hdf5 files to images(.jpg) directly.
# The program can deal with all of the h5 files in subfolds in "FLD".

######## How to use #########
# Four input parameters in file "run_readh5py.sh"
# Users should modify them before running
# workpath: path to folder "FLD", which contains original h5 files
# codepath: path of this script
# txt_output: "on" or "off", output txt data files or not
# img_output: "on" or "off", output jpg result files or not

######## Results #########
# If txt_output="on", txt files will be output to folder "txtdata" which has same level with "FLD"
# If img_output="on", jpg files will be output to folder "imgdata" which has same level with "FLD"

workpath="/Users/astrowjz/Desktop/read_h5/trans2silo/FLD"
codepath="/Users/astrowjz/Desktop/read_h5/trans2silo/plot2dslice"
txt_output="on"
img_output="on"

cd ${workpath}
if [ $txt_output = "on" ]
then
    mkdir ../txtdata >/dev/null 2>&1
fi
if [ $img_output = "on" ]
then
    mkdir ../imgdata >/dev/null 2>&1
fi
cd ${codepath}

python3 readh5.py ${workpath} ${n} ${txt_output} ${img_output}

echo " "
if [ $txt_output = "on" ]
then
    echo Txt files are stored into path: '"'${workpath/FLD/txtdata}'"'.
fi
if [ $img_output = "on" ]
then
    echo The figures are stored into path: '"'${workpath/FLD/imgdata}'"'.
fi
