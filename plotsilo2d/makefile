# name of the compiler 
SILO_INC=/public3/home/sc52879/astrowjz/flash/softwares/test_gcchdf5/silo_install/include
SILO_LIB=/public3/home/sc52879/astrowjz/flash/softwares/test_gcchdf5/silo_install/lib
HDF5_INC=/public3/home/sc52879/astrowjz/flash/softwares/test_gcchdf5/hdf5gcc_install/include
HDF5_LIB=/public3/home/sc52879/astrowjz/flash/softwares/test_gcchdf5/hdf5gcc_install/lib
# SILO_INC=/Users/anweiming/work/codes/visit_data/silo-4.10.2-bsd/include
# SILO_LIB=/Users/anweiming/work/codes/visit_data/silo-4.10.2-bsd/lib
# HDF5_INC=/Users/anweiming/work/codes/hdf5-1.10.5/hdf5/include
# HDF5_LIB=/Users/anweiming/work/codes/hdf5-1.10.5/hdf5/lib

# FC = mpif90 -c -O3 -I${SILO_INC} -I${HDF5_INC} 
# CC = mpicc -c -O3
# LINKER = mpif90 -O3 -L${SILO_LIB} -L${HDF5_LIB} -lsiloh5 -lhdf5
FC = gfortran -fdefault-real-8 -fdefault-double-8 -c -O3 -I${SILO_INC} -I${HDF5_INC} 
CC = gcc -c -O3
LINKER = -fdefault-real-8 -fdefault-double-8  -O3 -L${SILO_LIB} -L${HDF5_LIB} -lz -lsiloh5 -ldl -lhdf5
TEMP = gfortran
# Objects list

OBJS_BASE = \
# linklist.o getData.o initGrid.o solver.o bkg_solver.o 

OBJS_MAIN = test.o

OBJS = ${OBJS_BASE} ${OBJS_MAIN}

# Linkage rule
main :: ${OBJS} 
	${TEMP} ${OBJS} -o test.e ${LINKER}

clean ::
	rm *.o *.mod; rm test.e

# Compilation rules

# linklist.o : linklist.f03
# 	${FC} linklist.f03 -o linklist.o

# getData.o : getData.f03
# 	${FC} getData.f03 -o getData.o

# initGrid.o : initGrid.f03
# 	${FC} initGrid.f03 -o initGrid.o

# solver.o : solver.f03
# 	${FC} solver.f03 -o solver.o

# bkg_solver.o : bkg_solver.f03
# 	${FC} bkg_solver.f03 -o bkg_solver.o

# test.o : readh5.f03
# 	${FC} readh5.f03 -o test.o

test.o : plotsilo_2d.f03
	${FC} plotsilo_2d.f03 -o test.o

# test.o : protonimaging.f03
# 	${FC} protonimaging.f03 -o test.o

# test.o : mesh_vector3d.f03
# 	${FC} mesh_vector3d.f03 -o test.o

# test.o : point3d.f03
# 	${FC} point3d.f03 -o test.o

# test.o : mesh3d.f03
# 	${FC} mesh3d.f03 -o test.o

