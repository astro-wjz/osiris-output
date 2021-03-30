!! Creating silo file to generate 3-D mesh
!! Generate silo file of data.txt from PIC simulation
!! Users should input size of data (hei, col, row) and modify the name of files.

program mesh3d

    implicit none
      
    include "silo.inc"

    character(4) :: arg1, arg2
    character(6) :: arg3
    character(2) :: arg5
    character(18) :: arg6, arg7, arg8
    character(120) :: arg4
    character(7) :: arg9, arg10, arg11
    character(5) :: arg12
    character (len=120) :: filename
    character (len=120) :: workpath
    character (len=120) :: output_fname
    character (len=2) :: folder_name
    character (len=18) :: fname_re0, fname_re1, fname_im1
    character (len=10) :: var
    character (len=5) :: coord

    integer :: n_row, n_col
    integer :: col ,row, fac1, fac2
!     integer, parameter :: hei = 2400 ! colomns (1,1,:) 5 in test.txt
!     integer, parameter :: col = 10 ! height (1,:,1) 3
!     integer, parameter :: row = 2400 ! lines (:,1,1) 2

    integer :: dbfile, ierr, len_name
    real, dimension(3) :: coord_x, coord_y, coord_z
    integer :: i0,j0,k0,i,j,n
    real, dimension(:,:), allocatable :: data1, data2, data3, data4, data5, data6
    real, dimension(:,:), allocatable :: data0
    real :: pi 
    real :: phi, phi0, cosphi, sinphi, cos2phi, sin2phi, cossinphi
    real :: rmax, zmin, zmax

    j=1
    CALL get_command_argument(j, arg1)
    read(arg1,"(i4)")n_row
    j=2
    CALL get_command_argument(j, arg2)
    read(arg2,"(i4)")n_col
    j=3
    CALL get_command_argument(j, arg3)
    read(arg3,"(F6.2)")phi0
    j=4
    CALL get_command_argument(j, arg4)
    read(arg4,"(A120)")workpath
    j=5
    CALL get_command_argument(j, arg5)
    read(arg5,"(A2)")folder_name
    j=6
    CALL get_command_argument(j, arg6)
    read(arg6,"(A18)")fname_re0
    j=7
    CALL get_command_argument(j, arg7)
    read(arg7,"(A18)")fname_re1
    j=8
    CALL get_command_argument(j, arg8)
    read(arg8,"(A18)")fname_im1
    j=9
    CALL get_command_argument(j, arg9)
    read(arg9,"(F7.2)")rmax
    j=10
    CALL get_command_argument(j, arg10)
    read(arg10,"(F7.2)")zmin
    j=11
    CALL get_command_argument(j, arg11)
    read(arg11,"(F7.2)")zmax
    j=12
    CALL get_command_argument(j, arg12)
    read(arg12,"(A5)")coord

    pi = 4*atan(1.D0)

! OUTPUT FILE NAME
    output_fname = trim(workpath)//trim("/")//trim(folder_name)//trim("/")//trim(folder_name)//trim(fname_re0(8:14))//trim(".silo")
    output_fname = trim(output_fname)
    len_name = len_trim(output_fname)

! LOAD DATA FROM TXT FILES
    col = n_col
    row = n_row

    allocate(data1(row,col), data2(row,col), data3(row,col), data4(row,col), data5(row,col), data6(row,col))
    allocate(data0(row*2-1,col))

    filename = trim(workpath)//trim("/")//trim(fname_re0(1:7))//trim("/")//trim(fname_re0)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data1(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_re1(1:7))//trim("/")//trim(fname_re1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data2(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_im1(1:7))//trim("/")//trim(fname_im1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data3(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

! combine mode data
    phi = phi0/180*pi
    cosphi = cos(phi)*2
    sinphi = -sin(phi)*2
    do i0 = 1, row
        do j0 = 1, col
            data0(row-1+i0,j0) = data1(i0,j0) + data2(i0,j0)*cosphi + data3(i0,j0)*sinphi
        end do
    end do
    phi = phi0/180*pi + pi
    cosphi = cos(phi)*2
    sinphi = -sin(phi)*2
    do i0 = 2, row
        do j0 = 1, col
            data0(row+1-i0,j0) = data1(i0,j0) + data2(i0,j0)*cosphi + data3(i0,j0)*sinphi
        end do
    end do
    do j0 = 1, col
        data0(row, j0) = 0.0
    end do

! Create the Silo file
    ierr = dbcreate(output_fname, len_name, DB_CLOBBER, DB_LOCAL, "Quadvars in 3D", 14, DB_HDF5, dbfile)
    if(dbfile.eq.-1) then
        stop "Could not create Silo file!"
    endif

! Set axix min value, max value and node number. (Users input values)
    coord_z = (/real(zmin), real(zmax), real(col)/)
    coord_x = (/real(-rmax), real(rmax), real(2*row-1)/)
    print*, 'Create silo file  ', trim(output_fname), '  finished ! '

! Draw mesh and values
    var = "fz"
    call write_nodecent_quadvar(dbfile, coord_x, coord_z, data0, col, row, var)

! Draw bx and by
    fname_re0(2:2)="2"
    fname_re1(2:2)="2"
    fname_im1(2:2)="2"
    filename = trim(workpath)//trim("/")//trim(fname_re0(1:7))//trim("/")//trim(fname_re0)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data1(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_re1(1:7))//trim("/")//trim(fname_re1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data2(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_im1(1:7))//trim("/")//trim(fname_im1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data3(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    fname_re0(2:2)="3"
    fname_re1(2:2)="3"
    fname_im1(2:2)="3"
    filename = trim(workpath)//trim("/")//trim(fname_re0(1:7))//trim("/")//trim(fname_re0)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data4(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_re1(1:7))//trim("/")//trim(fname_re1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data5(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'

    filename = trim(workpath)//trim("/")//trim(fname_im1(1:7))//trim("/")//trim(fname_im1)
    filename = trim(filename)
    print*, 'Loading data ... '
    open(unit=99,file=filename)
    read(99,*) ( (data6(j0,i0), i0=1,col,1), j0=1,row,1 ) 
    close(unit=99)
    print*, trim(filename), ' data is imported successfully.'
    
    phi = phi0/180*pi
    if (phi0 >= 0 .and. phi0 <= 90) then
        fac1 = 1
        fac2 = -1
    else if (phi0 > 90 .and. phi0 < 180) then
        fac1 = -1
        fac2 = -1
    else if (phi0 >= 180 .and. phi0 <= 270) then
        fac1 = -1
        fac2 = 1
    else
        fac1 = 1
        fac2 = 1
    end if 
    if (coord == "carte") then
        cosphi = cos(phi)
        sinphi = sin(phi)
        cos2phi = 2*cosphi*cosphi
        sin2phi = 2-cos2phi
        cossinphi = -2*cosphi*sinphi
        do i0 = 1, row
            do j0 = 1, col
                data0(row-1+i0,j0) = (data1(i0,j0)*cosphi + data2(i0,j0)*cos2phi + data3(i0,j0)*cossinphi)*fac1 &
                    + ( - data4(i0,j0)*sinphi + data5(i0,j0)*cossinphi + data6(i0,j0)*sin2phi )*fac2
            end do
        end do
    else
        cosphi = cos(phi)*2
        sinphi = -sin(phi)*2
        do i0 = 1, row
            do j0 = 1, col
                data0(row-1+i0,j0) = data1(i0,j0) + data2(i0,j0)*cosphi + data3(i0,j0)*sinphi
            end do
        end do
    end if
    phi = phi0/180*pi + pi
    if (phi0+180 >= 0 .and. phi0+180 <= 90) then
        fac1 = 1
        fac2 = -1
    else if (phi0+180 > 90 .and. phi0+180 < 180) then
        fac1 = -1
        fac2 = -1
    else if (phi0+180 >= 180 .and. phi0+180 <= 270) then
        fac1 = -1
        fac2 = 1
    else
        fac1 = 1
        fac2 = 1
    end if 
    if (coord == "carte") then
        cosphi = cos(phi)
        sinphi = sin(phi)
        cos2phi = 2*cosphi*cosphi
        sin2phi = 2-cos2phi
        cossinphi = -2*cosphi*sinphi
        do i0 = 2, row
            do j0 = 1, col
                data0(row+1-i0,j0) = (data1(i0,j0)*cosphi + data2(i0,j0)*cos2phi + data3(i0,j0)*cossinphi)*fac1 &
                    + ( - data4(i0,j0)*sinphi + data5(i0,j0)*cossinphi + data6(i0,j0)*sin2phi )*fac2
            end do
        end do
    else
        cosphi = cos(phi)*2
        sinphi = -sin(phi)*2
        do i0 = 2, row
            do j0 = 1, col
                data0(row+1-i0,j0) = data1(i0,j0) + data2(i0,j0)*cosphi + data3(i0,j0)*sinphi
            end do
        end do
    end if
    do j0 = 1, col
        data0(row, j0) = 0.0
    end do
    
    if (coord == "carte") then
        var = "fx"
    else
        var = "fr"
    end if
    call write_nodecent_quadvar(dbfile, coord_x, coord_z, data0, col, row, var)

    phi = phi0/180*pi
    if (phi0 >= 90 .and. phi0 <= 180) then
        fac1 = 1
        fac2 = -1
    else if (phi0 > 180 .and. phi0 < 270) then
        fac1 = -1
        fac2 = -1
    else if (phi0 >= 270 .and. phi0 < 360) then
        fac1 = -1
        fac2 = 1
    else
        fac1 = 1
        fac2 = 1
    end if 
    if (coord == "carte") then
        cosphi = cos(phi)
        sinphi = sin(phi)
        cos2phi = 2*cosphi*cosphi
        sin2phi = 2-cos2phi
        cossinphi = -2*cosphi*sinphi
        do i0 = 1, row
            do j0 = 1, col
                data0(row-1+i0,j0) = (data1(i0,j0)*sinphi - data2(i0,j0)*cossinphi - data3(i0,j0)*sin2phi)*fac1 &
                    + (data4(i0,j0)*cosphi + data5(i0,j0)*cos2phi + data6(i0,j0)*cossinphi)*fac2
            end do
        end do
    else
        cosphi = cos(phi)*2
        sinphi = -sin(phi)*2
        do i0 = 1, row
            do j0 = 1, col
                data0(row-1+i0,j0) = data4(i0,j0) + data5(i0,j0)*cosphi + data6(i0,j0)*sinphi
            end do
        end do
    end if
    phi = phi0/180*pi + pi
    if (phi0+180 >= 90 .and. phi0+180 <= 180) then
        fac1 = 1
        fac2 = -1
    else if (phi0+180 > 180 .and. phi0+180 < 270) then
        fac1 = -1
        fac2 = -1
    else if (phi0+180 >= 270 .and. phi0+180 < 360) then
        fac1 = -1
        fac2 = 1
    else
        fac1 = 1
        fac2 = 1
    end if 
    if (coord == "carte") then
        cosphi = cos(phi)
        sinphi = sin(phi)
        cos2phi = 2*cosphi*cosphi
        sin2phi = 2-cos2phi
        cossinphi = -2*cosphi*sinphi
        do i0 = 2, row
            do j0 = 1, col
                data0(row+1-i0,j0) = (data1(i0,j0)*sinphi - data2(i0,j0)*cossinphi - data3(i0,j0)*sin2phi)*fac1 &
                    + (data4(i0,j0)*cosphi + data5(i0,j0)*cos2phi + data6(i0,j0)*cossinphi)*fac2
            end do
        end do
    else
        cosphi = cos(phi)*2
        sinphi = -sin(phi)*2
        do i0 = 2, row
            do j0 = 1, col
                data0(row+1-i0,j0) = data4(i0,j0) + data5(i0,j0)*cosphi + data6(i0,j0)*sinphi
            end do
        end do
    end if
    do j0 = 1, col
        data0(row, j0) = 0.0
    end do

    deallocate(data1,data2,data3,data4,data5,data6)

    if (coord == "carte") then
        var = "fy"
    else
        var = "fphi"
    end if
    
    call write_nodecent_quadvar(dbfile, coord_x, coord_z, data0, col, row, var)

! Close the Silo file.
    ierr = dbclose(dbfile)

    deallocate(data0)

end program mesh3d


!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!						 !!
!!		NODE CENTRE		 !!
!!						 !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!

subroutine write_nodecent_quadvar(dbfile, coord_x, coord_z, data0, col, row, var)

    implicit none

    include "silo.inc"

    integer :: dbfile, err, ierr, dims(2), ndims, optlistid
    real, dimension(3) :: coord_x, coord_z
    real :: xmin, xmax, zmin, zmax, dx, dz
    integer :: xnd, znd, i, j, k
    real, allocatable :: x(:), z(:)!, nodal(:,:,:)
    character(len=10), INTENT(INOUT) :: var
    real :: time

!     integer, parameter :: hei = 100
!     integer, parameter :: col = 80
!     integer, parameter :: row = 40
    integer :: col, row, len_var
    real, dimension(row*2-1,col) :: data0

    len_var = len_trim(var)

    xmin = coord_x(1)                           ! min value
    xmax = coord_x(2)                           ! max value
    xnd  = int(coord_x(3))                      ! cell number
    dx   = (xmax - xmin)/(xnd-1)  ! cell size
    
    zmin = coord_z(1)
    zmax = coord_z(2)
    znd  = int(coord_z(3))
    dz   = (zmax - zmin)/(znd-1)

    ndims = 2
    dims(1:2) = (/xnd, znd/)  ! mesh size

    allocate(x(xnd), z(znd))

    do i = 0, xnd-1
        x(i+1) = xmin + dx*i 
    enddo
    do i = 0, znd-1
        z(i+1) = zmin + dz*i 
    enddo

!   Create an option list and add spherical coordinate to it.

    err = dbmkoptlist(3, optlistid)

!   spherical coordinate (DB_CARTESIAN, DB_CYLINDRICAL, DB_SPHERICAL, DB_NUMERICAL, or DB_OTHER)
!     err = dbaddiopt(optlistid, DBOPT_COORDSYS, DB_CYLINDRICAL)    
! zone face type (DB_RECTILINEAR or DB_CURVILINEAR)
! 	err = dbaddiopt(optlistid, DBOPT_FACETYPE, DB_CURVILINEAR)	
! Add axis labels and units
    err = dbaddcopt(optlistid, DBOPT_XLABEL, 'r', 1)
! 	err = dbaddcopt(optlistid, DBOPT_XUNITS, "kPa", 3)
!     err = dbaddcopt(optlistid, DBOPT_YLABEL, 'phi', 3)
! 	err = dbaddcopt(optlistid, DBOPT_YUNITS, "Celsius", 7)
    err = dbaddcopt(optlistid, DBOPT_YLABEL, 'z', 1)
! 	! Add units to color bar
! 	err = dbaddcopt(optlistid, DBOPT_UNITS, "m/s", 3)
! 	! Saving cycle and time using an option list.
! 	err = dbaddiopt(optlistid, DBOPT_CYCLE, cycle) ! cycle: int
! 	err = dbadddopt(optlistid, DBOPT_DTIME, dtime) ! dtime: double
! 	err = dbadddopt(optlistid, DBOPT_TIME, time)  ! time: float


    ! 3D rectilinear mesh
    err = dbputqm (dbfile, "quadmesh", 8, "xc", 2, "yc", 2, "zc", 2, &
        x, z, DB_F77NULL, dims, ndims, DB_DOUBLE, DB_COLLINEAR, optlistid, ierr)

!     deallocate(x, y, z)
    ! 3D curvilinear mesh
!     err = dbputqm (dbfile, "quadmesh", 8, "xc", 2, "yc", 2, "zc", 2, &
!     	x, y, z, dims, ndims, DB_FLOAT, DB_NONCOLLINEAR, DB_F77NULL, ierr)

! 	allocate(nodal(xnd, ynd, znd))

! Set scalar value into 3D rectilinear mesh
    time = 0.0
    err = dbadddopt(optlistid, DBOPT_TIME, time)  ! time: float
    err = dbputqv1(dbfile, var, len_var, "quadmesh", 8, data0, dims, &
          ndims, DB_F77NULL, 0, DB_DOUBLE, DB_NODECENT, optlistid, ierr)

!   Free the option list.
    err = dbfreeoptlist(optlistid)

    print*, 'Output ', trim(var), ' to silo file finished ! '
    deallocate(x, z)
!     deallocate(nodal)

end subroutine write_nodecent_quadvar

