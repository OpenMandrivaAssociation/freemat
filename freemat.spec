# Cyclic dependencies
%define		_disable_ld_no_undefined	1

%define		freemat_dir			%{_datadir}/FreeMat

%define		oname		FreeMat
%define		oversion	4.1

Name:		freemat
Group:		Sciences/Mathematics
License:	GPL
Summary:	Rapid engineering, scientific prototyping and data processing
# Real version is 4.1 final but extra .1 is needed up update from 4.1.0.20110113
Version:	4.1.1
Release:	1
URL:		http://freemat.sourceforge.net
Source0:	%{oname}-%{oversion}-Source.tar.gz
Source1:	http://www.netlib.org/lapack/lapack-3.2.2.tgz
Source2:	http://www.netlib.org/clapack/CLAPACK-3.1.1/F2CLIBS/libf2c/pow_ii.c

#-------------------------------------------------------------------------------
BuildRequires:	amd-devel
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	f2c
BuildRequires:	ffcall-devel
BuildRequires:	fftw-devel
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	libatlas-devel
BuildRequires:	ncurses-devel
BuildRequires:	pcre-devel
BuildRequires:	portaudio-devel
BuildRequires:	qt4-devel
BuildRequires:	umfpack-devel
BuildRequires:	zlib-devel

#-------------------------------------------------------------------------------
Requires:	libatlas

#-------------------------------------------------------------------------------
Patch1:		FreeMat-4.1-missing.patch
Patch2:		FreeMat-4.1-blas.patch
Patch3:		FreeMat-4.1-freemat_dir.patch
Patch4:		freemat-4.1-fixes.patch
Patch5:		freemat-4.1-use_llvm.patch
Patch6:		FreeMat-4.1-linkage.patch


#-------------------------------------------------------------------------------
%description
FreeMat is a free environment for rapid engineering and scientific prototyping
and data processing. It is similar to commercial systems such as MATLAB from
Mathworks, and IDL from Research Systems, but is Open Source.

#-------------------------------------------------------------------------------
%prep
%setup -q -n %{oname}-%{oversion}-Source -a 1

for file in `find . -name CMake\*.txt`; do dos2unix $file; done
find . -name CMakeCache.txt -delete
find . -type f -name '*.moc.cpp' -delete
find . -type f -name 'add.so' -delete

# undefined references
%patch1		-p1
cp -f %{SOURCE2} libs/libMath/libLAPACK_C
for f in					\
	dlaed6					\
	dlamrg					\
	dlasd{0,1,2,3,4,5,6,7,8,a,q,t}		\
	slaed6					\
	slamrg slasd{0,1,2,3,4,5,6,7,8,a,q,t}	\
	sbdsdc; do
    f2c lapack-3.2.2/SRC/$f.f
    mv $f.c libs/libMath/libLAPACK_C
done

%patch2		-p1
perl -pi -e 's|@@FREEMAT_DIR@@|%{freemat_dir}|;'	\
	libs/libMath/libDynBlas/blas_dyn_link.cpp

%patch3		-p1

%patch4 -p0
%patch5 -p0
%patch6 -p1

#-------------------------------------------------------------------------------
%build
(
%cmake	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DUSE_LLVM=OFF \
	-DUSE_ITK=OFF \
	-DFORCE_BUNDLED_PCRE=OFF \
	-DFORCE_BUNDLED_UMFPACK=OFF \
	-DFORCE_BUNDLED_PORTAUDIO=OFF \
	-DFORCE_BUNDLED_ZLIB=OFF \
	-DFORCE_BUNDLED_AMD=OFF
%make
)

#-------------------------------------------------------------------------------
%install
%makeinstall_std -C build

#-------------------------------------------------------------------------------
%files
%{_bindir}/*
%{freemat_dir}

