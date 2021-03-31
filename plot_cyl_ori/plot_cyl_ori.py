# @Time    : 2021-03-30
# @Author  : Wang Jianzhao
# @Company : Department of Astronomy, Beijing Normal University

"""
Description:
    Program for vasualizing hdf5 result files from Osiris cyl modes code.
    
How to use:
    Two input parameters in file "run_cyl_ori.sh"
    Users should modify them before running.
    workpath: path to folder "FLD", which contains original h5 files
    phi: angle of the slice along z axis

Output:
    Image 'png' files will be output to folder "RESULTS" which has same level with "FLD"

Advanced:
    Users can set the images and colorbar parameters by modifying line 126 to line 136

"""

import h5py
import numpy as np
from sys import argv
import subprocess
import matplotlib
matplotlib.use('Agg') # Do not show images, only save them
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
from os import system as sys

script_name = argv[0]   # script name
workpath = argv[1]      # workpath of data files
phi = argv[2]           # angle of the slice along z axis

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

def get_data_path(mode_path, emf_name):
    """return full path of all modes of data file
    Args:
        modepath: a list of full path of all modes
        emf_name: the folder contains the data file need to be processed
    Return:
        datapath_list: full path of all modes of data file
        datafile_list: all data file names of all modes
    """
    datapath_list=[]
    datafile_list=[]
    for j in mode_path:
        datapath = j + emf_name + "/"
        data_file_list, data_file_num = input_file(datapath)
        for i in data_file_list:
            datafile_name = "%s"%(str(i, "utf-8")).replace("\n", "")
            datafile_list.append(datafile_name)
        datapath_list.append(datapath)
    return datapath_list, datafile_list

def load_data(filepath, datafilename):
    """load data from h5 files
    Args:
        filepath: path to h5 files
        datafilename: the name single h5 file
    Return:
        filename: full path of data file
        data: original data of filename
        dset: the name of variable in data file
    Raises:
        Print Errors if open h5 file failed;
    """
    filename = filepath + datafilename
    try:
        f = h5py.File(filename, 'r')
        para_a,para_b,dset = f.keys()
        d_set = f[dset]
        data = np.array(d_set[:,:])
        f.close()
    except:
        print("Open file", datafilename, "failed !")
    return filename, data, dset

def init_outpath(workpath, emf_name):
    """initial workpath and build some folders
    Args:
        workpath: path to folder "FLD", which contains original h5 files
        emf_name: folders contains h5 files, like b1_cyl_m/
    Return:
        res_path: path to RESULTS/ which contains output images
    """
    res_path = "%s"%(workpath.replace("/FLD","/RESULTS/"))
    sys("mkdir %s >/dev/null 2>&1"%res_path)
    for i in emf_name:
        outpath = res_path + i
        sys("rm -rf %s >/dev/null 2>&1"%outpath)
        sys("mkdir %s >/dev/null 2>&1"%outpath)
    return res_path

def output_file(res_path, filename, data, dset):
    """output images from data
    Args:
        res_path: path to RESULTS/ which contains output images
        filename: name of data file
        data: processed data of each mode
        dset: the name of variable in data file
    Return:
        None
    Raises:
        Print Errors if output result image failed.
    """
    outname = filename[0:2] + filename[-10:-2] + "png"
    outpath = res_path + dset + "/" + outname
    try:
        fig = plt.figure()
        ax = fig.gca()
        im = ax.imshow(data,cmap="bwr",vmax=10,vmin=-10)
        plt.title(outname[:outname.index(".")])
        cb = plt.colorbar(im,orientation='horizontal')
        tick_locator = ticker.MaxNLocator(nbins=9)
        cb.locator = tick_locator
        cb.set_ticks([-10,-7.5,-5,-2.5,0,2.5,5,7.5,10])
        cb.update_ticks()
        plt.savefig(outpath)
        plt.close()
    except:
        print("Write file", outname, "failed!")       

def progress_bar(order_num, sumf):
    """output images from data
    Args:
        order_num: The nth picture has been processed
        sumf: total number of h5 files need to be processed
    Return:
        None
    """
    percent = int(order_num/sumf*100)
    num = percent // 2
    if order_num == sumf:
        process = "\r[%3s%%]: [%-50s]\n" % (percent, '=' * num)
    else:
        process = "\r[%3s%%]: [%-50s]" % (percent, '=' * num)
    print(process, end='', flush=True)


#--- main program ---#

phi = float(phi)/180.0*math.pi

mode_name, mode_num = input_file(workpath)
mode_path_list = list()  # all paths to each mode folder
for i in range(mode_num):
    mode_name[i] = "%s"%(str(mode_name[i], "utf-8")).replace("\n", "") # MODE-0-RE
    mode_path = "%s"%(workpath) + "/" + "%s"%(mode_name[i]) + "/" # /Path/to/MODE-0-RE
    mode_path_list.append(mode_path) # /PATH/TO/[MODE-0-RE, MODE-1-IM, MODE-1-RE]

emf_name, emf_num = input_file(mode_path_list[0])
for i in range(emf_num):
    emf_name[i] = "%s"%(str(emf_name[i], "utf-8")).replace("\n", "") # b2_cyl_1

#--- total file number ---#
mode_0_path = mode_path_list[0] + emf_name[0]
mode_0_data_list, data_num = input_file(mode_0_path)
sumf = data_num * emf_num
print("Totally %d files to process, please waite a minute ... "%sumf)

#--- initial path ---#
res_path = init_outpath(workpath, emf_name)
order_num = 0 # The nth picture has been processed

#--- Cylindrical mode composition ---#
for i in range(emf_num):
    emf_path_list, data_file_list = get_data_path(mode_path_list,emf_name[i])
    for j in range(data_num):
        filepath, data0, var_name = load_data(emf_path_list[0],data_file_list[j])
        for k in range(1,mode_num):
            if k%2 == 1:
                filepath, data1, var_name = load_data(emf_path_list[k],data_file_list[j+k*mode_num])
                data0 = data0 + 2*math.cos(phi*k)*data1
            else:
                filepath, data1, var_name = load_data(emf_path_list[k],data_file_list[j+k*mode_num])
                data0 = data0 - 2*math.sin(phi*k)*data1
        output_file(res_path, data_file_list[j], data0, var_name)

#--- Show progress bar ---#
        order_num = order_num + 1
        progress_bar(order_num, sumf)
