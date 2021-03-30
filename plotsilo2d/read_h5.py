import h5py
import numpy as np
from sys import argv

script, n, workpath = argv
n = int(n)  # number of h5 files
# workpath = os.path.dirname(os.path.realpath(__file__))
#workpath = "/public3/home/sc52879/astrowjz/osiris/astrowjz/cyl01/MS/FLD"
filepath = ["/MODE-0-RE/", "/MODE-1-RE/", "/MODE-1-IM/", "/MODE-2-RE/", "/MODE-2-IM/"]
dset_name = ["b1_cyl_m", "b2_cyl_m", "b3_cyl_m", "e1_cyl_m", "e2_cyl_m", "e3_cyl_m"]
mode_name = ["-0-re-", "-1-re-", "-1-im-", "-2-re-", "-2-im-"]
out_name = ["b1_re_0", "b1_re_1", "b1_im_1", "b2_re_0", "b2_re_1", "b2_im_1", \
            "b3_re_0", "b3_re_1", "b3_im_1", "e1_re_0", "e1_re_1", "e1_im_1", \
            "e2_re_0", "e2_re_1", "e2_im_1", "e3_re_0", "e3_re_1", "e3_im_1" ]
filetail = ".h5"
outtail = ".txt"

# for key in f.keys():      
#     print(f[key].name)      
for j in range(0,6):
    for i in range(0,n):
        number = '%06d' % i
        # read hdf5 data files mode 0 re
        filename = "%s"%(workpath) + "%s"%(filepath[0]) + "%s"%(dset_name[j]) + "/" + "%s"%(dset_name[j]) + "%s"%(mode_name[0]) + "%s"%(number) + "%s"%(filetail)
        f = h5py.File(filename, 'r')
        print("File", filename, "is opened!")
        dset = f[dset_name[j]]
        data = np.array(dset[:,:])
        outname = "%s"%(workpath) + "/" + "%s"%(out_name[0+j*3]) + "/" + "%s"%(out_name[0+j*3]) + "-" + "%s"%(number) + "%s"%(outtail)
        np.savetxt(outname, data)
        print("File", outname, "is written!")
        # read hdf5 data files mode 1 re
        filename = "%s"%(workpath) + "%s"%(filepath[1]) + "%s"%(dset_name[j]) + "/" + "%s"%(dset_name[j]) + "%s"%(mode_name[1]) + "%s"%(number) + "%s"%(filetail)
        f = h5py.File(filename, 'r')
        print("File", filename, "is opened!")
        dset = f[dset_name[j]]
        data = np.array(dset[:,:])
        outname = "%s"%(workpath) + "/" + "%s"%(out_name[1+j*3]) + "/" + "%s"%(out_name[1+j*3]) + "-" + "%s"%(number) + "%s"%(outtail)
        np.savetxt(outname, data)
        print("File", outname, "is written!")
        # read hdf5 data files mode 1 im
        filename = "%s"%(workpath) + "%s"%(filepath[2]) + "%s"%(dset_name[j]) + "/" + "%s"%(dset_name[j]) + "%s"%(mode_name[2]) + "%s"%(number) + "%s"%(filetail)
        f = h5py.File(filename, 'r')
        print("File", filename, "is opened!")
        dset = f[dset_name[j]]
        data = np.array(dset[:,:])
        outname = "%s"%(workpath) + "/" + "%s"%(out_name[2+j*3]) + "/" + "%s"%(out_name[2+j*3]) + "-" + "%s"%(number) + "%s"%(outtail)
        np.savetxt(outname, data)
        print("File", outname, "is written!")
