# @Time    : 2021-04-13
# @Author  : Wang Jianzhao
# @Company : Department of Astronomy, Beijing Normal University

"""
Description:
    Program for vasualizing hdf5 result files from Osiris cyl modes decomposition code, 
    and combine a slice along z-driction at any angle. Especially for plotting density files.
    
How to use:
    Two input parameters in file "run_cyl_ori.sh"
    Users should modify them before running.
    workpath: path to folder "FLD", which contains original h5 files
    phi: angle of the slice along z axis
    rmax: the real max length of r direction
    zmin: the real min position of z direction
    zmax: the real max position of z direction
    npr: total amount of points along r direciton
    npz: total amount of points along z direction

Output:
    Images and movies will be output to folder "RESULTS" which has same level with "DENSITY"

Advanced:
    Users can set the images and colorbar parameters by modifying function output_file_i() and output_file_e()

"""

import h5py
import numpy as np
from sys import argv
import subprocess
import matplotlib
matplotlib.use('Agg') # Do not show images, only save them
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import math
from os import system as sys
from cv2 import cv2

script_name = argv[0]   # script name
workpath = argv[1]      # workpath of data files
phi = float(argv[2])           # angle of the slice along z axis
rmax = float(argv[3])
zmin = float(argv[4])
zmax = float(argv[5])
np_r = float(argv[6])
np_z = float(argv[7])

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

def init_outpath(workpath, part_name):
    """initial workpath and build some folders
    Args:
        workpath: path to folder "DENSITY", which contains original h5 files
        part_name: folder contains mode subfolders, like electrons/
    Return:
        res_path: path to RESULTS/ which contains output images
    """
    res_path = "%s"%(workpath.replace("/DENSITY","/RESULTS/"))
    sys("mkdir %s >/dev/null 2>&1"%res_path)
    outpath = res_path + part_name
    sys("rm -rf %s >/dev/null 2>&1"%outpath)
    sys("mkdir %s >/dev/null 2>&1"%outpath)
    return res_path

def output_file_i(res_path, filename, data, pname, rmax, zmin, zmax, np_r, np_z, datamax, datamin):
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
    outname = pname + filename[-10:-2] + "png"
    outpath = res_path + pname + "/" + outname

    try:
        # fig = plt.figure()
        # plt.rcParams['figure.figsize'] = (12.0, 8.0)

        xlab = np.linspace(-rmax,rmax,int(2*np_r-1))
        ylab = np.linspace(zmin,zmax,int(np_z))
        xx,yy = np.meshgrid(xlab,ylab)
        # fig, ax = plt.subplots()
        # c = ax.pcolormesh(xx,yy,data,cmap='jet',shading='auto')
        # fig.colorbar(c, ax=ax)

        fig = plt.figure()
        im = plt.pcolormesh(xx,yy,data,cmap='jet',shading='auto',vmax=50,vmin=0)
        cb = plt.colorbar(im)
        cb.set_label('Particles')

        # ax = fig.gca()
        # im = ax.imshow(data)#,cmap="bwr",vmax=10,vmin=-10)
        # def changex(temp, position):
        #     return int(temp*scale_r)
        # def changey(temp, position):
        #     return int(temp/scale_z)
        plt.title(outname[:outname.index(".")])
        plt.text(65, 52, "max: %.2f"%datamax, size=10)
        plt.text(65, -14, "min: %.2f"%datamin, size=10)
        # cb = plt.colorbar(im)#,orientation='horizontal')
        # my_y_ticks = np.arange(0 ,np_z+0.01, dny)
        # # my_x_ticks = np.arange(0, rmax, 10)
        # # plt.xticks(my_x_ticks)
        # plt.yticks(my_y_ticks)
        # plt.gca().xaxis.set_major_formatter(FuncFormatter(changex))
        # plt.gca().yaxis.set_major_formatter(FuncFormatter(changey))
        # ax.set_aspect(scale_ax)
        # new_ticks = np.linspace(-10, 500.1, 10)
        # plt.yticks(new_ticks)
        # tick_locator = ticker.MaxNLocator(nbins=6)
        # cb.locator = tick_locator
        # cb.set_ticks([0,10,20,30,40,50])
        # cb.update_ticks()
        plt.savefig(outpath)
        plt.close()
    except:
        print("Write file", outname, "failed!")       

def output_file_e(res_path, filename, data, pname, rmax, zmin, zmax, np_r, np_z, datamax, datamin):
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
    outname = pname + filename[-10:-2] + "png"
    outpath = res_path + pname + "/" + outname

    try:
        # fig = plt.figure()
        # plt.rcParams['figure.figsize'] = (12.0, 8.0)

        xlab = np.linspace(-rmax,rmax,int(2*np_r-1))
        ylab = np.linspace(zmin,zmax,int(np_z))
        xx,yy = np.meshgrid(xlab,ylab)
        # fig, ax = plt.subplots()
        # c = ax.pcolormesh(xx,yy,data,cmap='jet',shading='auto')
        # fig.colorbar(c, ax=ax)

        fig = plt.figure()
        im = plt.pcolormesh(xx,yy,data,cmap='jet',shading='auto',vmax=0,vmin=-150)
        cb = plt.colorbar(im)
        cb.set_label('Particles')
        plt.title(outname[:outname.index(".")])
        plt.text(65, 52, "max: %.2f"%datamax, size=10)
        plt.text(65, -14, "min: %.2f"%datamin, size=10)
        # cb = plt.colorbar(im)#,orientation='horizontal')
        tick_locator = ticker.MaxNLocator(nbins=6)
        cb.locator = tick_locator
        cb.set_ticks([0,-30,-60,-90,-120,-150])
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

def output_video(res_path, pname):
    """output videos from images
    Args:
        res_path: path to RESULTS/ which contains output images
        emf_name: folders contains h5 files, like b1_cyl_m/
    Return:
        None
    """
    outpath = res_path + pname + "/"
    outname = outpath + pname + ".mp4"
    filelist, filenum = input_file(outpath)
    for i in range(filenum):
        filelist[i] = outpath + "%s"%(str(filelist[i], "utf-8")).replace("\n", "")
    test = cv2.imread(filelist[0])
    size = test.shape[:2]
    forcc=cv2.VideoWriter_fourcc(*'mp4v')
    videowrite = cv2.VideoWriter(outname,forcc,10,(size[1],size[0]))
    img_array=[]
    for filename in filelist:
        img = cv2.imread(filename)
        img_array.append(img)
    for i in range(filenum):
        videowrite.write(img_array[i])
    videowrite.release()


#--- main program ---#

phi = float(phi)/180.0*math.pi

part_name, part_num = input_file(workpath)
for p_num in range(part_num):
    part_name[p_num] = "%s"%(str(part_name[p_num], "utf-8")).replace("\n", "")

    part_path = "%s"%(workpath) + "/" + part_name[p_num]

    mode_name, mode_num = input_file(part_path)
    mode_path_list = list()  # all paths to each mode folder
    for i in range(mode_num):
        mode_name[i] = "%s"%(str(mode_name[i], "utf-8")).replace("\n", "") # MODE-0-RE
        mode_path = "%s"%(part_path) + "/" + "%s"%(mode_name[i]) + "/" # /Path/to/MODE-0-RE/
        mode_path_list.append(mode_path) # /PATH/TO/[MODE-0-RE, MODE-1-IM, MODE-1-RE]/

    charge_name, charge_num = input_file(mode_path_list[0])
    for i in range(charge_num):
        charge_name[i] = "%s"%(str(charge_name[i], "utf-8")).replace("\n", "") # charge_cyl_m 

    #--- total file number ---#
    mode_0_path = mode_path_list[0] + charge_name[0]
    mode_0_data_list, data_num = input_file(mode_0_path)
    sumf = data_num * charge_num
    print("Particle %s"%part_name[p_num], " has %d files to process, please waite a minute ... " %sumf)

    #--- initial path ---#
    res_path = init_outpath(workpath, part_name[p_num])
    order_num = 0 # The nth picture has been processed

    #--- Cylindrical mode composition ---#
    for i in range(charge_num):
        try:
            data_path_list, data_file_list = get_data_path(mode_path_list,charge_name[i])
            for j in range(data_num):
                filepath, data0, var_name = load_data(data_path_list[0],data_file_list[j])
                rl, zl = data0.shape # 160, 320
                data = np.empty(shape=(zl,2*rl-1))
                for k in range(1,mode_num):
                    if k%2 == 1:
                        fac = 2*math.cos(phi*(2*k-1))
                        filepath, data1, var_name = load_data(data_path_list[k],data_file_list[j+k*data_num])
                        data0 = data0 + fac*data1
                    else:
                        fac = - 2*math.sin(phi*k/2)
                        filepath, data2, var_name = load_data(data_path_list[k],data_file_list[j+k*data_num])
                        data0 = data0 + fac*data1
                datamax = np.amax(data0)
                datamin = np.amin(data0)
                for ii in range(zl):
                    for jj in range(rl):
                        data[ii, jj+rl-1] = data0[jj,ii]
                filepath, data0, var_name = load_data(data_path_list[0],data_file_list[j])
                for k in range(1,mode_num):
                    if k%2 == 1:
                        fac = 2*math.cos((phi+math.pi)*(2*k-1))
                        # filepath, data1, var_name = load_data(data_path_list[k],data_file_list[j+k*data_num])
                        data0 = data0 + 2*math.cos((phi+math.pi)*k)*data1
                    else:
                        fac = - 2*math.sin((phi+math.pi)*k/2)
                        # filepath, data1, var_name = load_data(data_path_list[k],data_file_list[j+k*data_num])
                        data0 = data0 - fac*data2
                for ii in range(zl):
                    for jj in range(1,rl):
                        data[ii, rl-jj-1] = data0[jj,ii]
                if p_num==0:
                    output_file_i(res_path, data_file_list[j], data, part_name[p_num], rmax, zmin, zmax, np_r, np_z, datamax, datamin)
                else:
                    output_file_e(res_path, data_file_list[j], data, part_name[p_num], rmax, zmin, zmax, np_r, np_z, datamax, datamin)
                #--- Show progress bar ---#
                order_num = order_num + 1
                progress_bar(order_num, sumf)
            #--- Create videos ---*
            output_video(res_path, part_name[p_num])
        except:
            print("Something wrong in main program !")


