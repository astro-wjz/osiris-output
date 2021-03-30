# @Time    : 2021-03-29
# @Author  : Wang Jianzhao
# @Company : Department of Astronomy, Beijing Normal University

"""
Description:
    Program for formatting Osiris 2D hdf5 files to txt data files.
    Program for plotting Osiris 2D hdf5 files to images(.jpg) directly.
    The program can deal with all of the h5 files in subfolds in "FLD".

How to use:
    Four input parameters in file "run_readh5py.sh"
    Users should modify them before running
    workpath: path to folder "FLD", which contains original h5 files
    codepath: path of this script
    txt_output: "on" or "off", output txt data files or not
    img_output: "on" or "off", output jpg result files or not

Results:
    If txt_output="on", txt files will be output to folder "txtdata" which has same level with "FLD"
    If img_output="on", jpg files will be output to folder "imgdata" which has same level with "FLD"

Advanced:
    Users can set the images and colorbar parameters by modifying line 72 to line 81

"""

import h5py
import numpy as np
from sys import argv
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

script_name = argv[0]   # script name
workpath = argv[1]      # workpath of data files
ifTxt = argv[2]         # output txt data files or not
ifImage = argv[3]       # output jpg result files or not

def input_file(path):
    """List all files contained in the folder.

    Args:
        path: path to the folder which users want to list all files.
    
    Returns:
        folder_list: a list contains all files of this "path";
        n: total number of files be listed, which type is integer.
    """
    process = subprocess.Popen("ls %s"%(path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    folder_list = process.stdout.readlines()
    n = len(folder_list)
    return folder_list, n

def output_file(filepath,datafile):
    """Deal with h5 files
    If txt_output="on", txt files will be output to folder "txtdata" which has same level with "FLD"
    If img_output="on", jpg files will be output to folder "imgdata" which has same level with "FLD"

    Args:
        filepath: path to h5 files
        datafile: the name single h5 file

    Return:
        None

    Raises:
        Print Errors if open h5 file failed;
        Print Errors if output txt file failed;
        Print Errors if output result image failed.
    """
    filename = "%s"%(filepath.replace("\n", "")) + "/" + datafile
    try:
        f = h5py.File(filename, 'r')
        para_a,para_b,dset = f.keys()
        d_set = f[dset]
        data = np.array(d_set[:,:])
        f.close()
    except:
        print("Open file", datafile, "failed!")

    if ifTxt == "on":
        outname = "%s"%(filename.replace("/FLD","/txtdata/"))
        outname = outname[:outname.index("//")] + "/" + datafile
        outname = "%s"%(outname.replace(".h5",".txt"))
        try:
            np.savetxt(outname, data)
        except:
            print("Write file", outname, "failed!")

    if ifImage == "on":
        try:
            outname = "%s"%(filename.replace("/FLD","/imgdata/"))
            outname = outname[:outname.index("//")] + "/" + datafile
            outname = "%s"%(outname.replace(".h5",".png"))
            fig = plt.figure()
            ax = fig.gca()
            im = ax.imshow(data,cmap="bwr",vmax=10,vmin=-10)
            plt.title(datafile[:datafile.index(".")])
            cb = plt.colorbar(im,orientation='horizontal')
            tick_locator = ticker.MaxNLocator(nbins=9)
            cb.locator = tick_locator
            cb.set_ticks([-10,-7.5,-5,-2.5,0,2.5,5,7.5,10])
            cb.update_ticks()
            plt.savefig(outname)
            plt.close()
        except:
            print("Write file", outname, "failed!")

# main program
# for i in data_folder:
#     filepath = "%s"%(workpath) + "/" + "%s"%(str(i, "utf-8"))
#     data_file, file_num = input_file(filepath)
#     for j in data_file:
#         real_name = "%s"%(str(j, "utf-8").replace("\n", ""))
#         output_file(filepath, real_name)

data_folder, folder_num = input_file(workpath)

sumf = 0  # total number of h5 files
temp = 0
for i in data_folder:
    filepath = "%s"%(workpath) + "/" + "%s"%(str(i, "utf-8"))
    data_file, file_num = input_file(filepath)
    sumf = sumf + file_num

# main program
print("Reading and processing totally", sumf, "files ... ")
for i in data_folder:
    filepath = "%s"%(workpath) + "/" + "%s"%(str(i, "utf-8"))
    data_file, file_num = input_file(filepath)
    for j in data_file:
        real_name = "%s"%(str(j, "utf-8").replace("\n", ""))
        output_file(filepath, real_name)
        temp = temp + 1
        percent = int(temp/sumf*100)
        num = percent // 2
        if temp == sumf:
            process = "\r[%3s%%]: [%-50s]\n" % (percent, '=' * num)
        else:
            process = "\r[%3s%%]: [%-50s]" % (percent, '=' * num)
        print(process, end='', flush=True)
