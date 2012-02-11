# Cyclic dependencies
%define		_disable_ld_no_undefined	1

%define		freemat_dir			%{_datadir}/FreeMat

Name:		freemat
Group:		Sciences/Mathematics
License:	GPL
Summary:	rapid engineering, scientific prototyping and data processing
Version:	4.1.0.20110113
Release:	%mkrel 2
URL:		http://freemat.sourceforge.net
# svn co https://freemat.svn.sourceforge.net/svnroot/freemat/trunk/FreeMat freemat
# cp -far freemat freemat-4.1.0.20110113
# cd freemat-4.1.0.20110113
# find . -name .svn -exec rm -fr {} \; 2>/dev/null
# cd ..
# tar Jcf freemat-4.1.0.20110113.tar.xz freemat-4.1.0.20110113
Source0:	%{name}-%{version}.tar.xz
Source1:	http://www.netlib.org/lapack/lapack-3.2.2.tgz
Source2:	http://www.netlib.org/clapack/CLAPACK-3.1.1/F2CLIBS/libf2c/pow_ii.c
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#-------------------------------------------------------------------------------
BuildRequires:	amd-devel
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	f2c
BuildRequires:	ffcall-devel
BuildRequires:	fftw-devel
BuildRequires:	gcc-gfortran
BuildRequires:	GL-devel
BuildRequires:	libatlas-devel
BuildRequires:	llvm
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

#-------------------------------------------------------------------------------
%description
FreeMat is a free environment for rapid engineering and scientific prototyping
and data processing. It is similar to commercial systems such as MATLAB from
Mathworks, and IDL from Research Systems, but is Open Source.

#-------------------------------------------------------------------------------
%prep
%setup -q -n %{name}-%{version} -a 1

for file in `find . -name CMake\*.txt`; do dos2unix $file; done

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

#-------------------------------------------------------------------------------
%build
(
%cmake	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}		\
	-DBUILD_SHARED_LIBS:BOOL=OFF
%make
)

#-------------------------------------------------------------------------------
%install

# avoid make install failure (proper correction should be regenerate .pdf file)
mv -f help/latex/FreeMat-4.{0,1}.pdf

%makeinstall_std -C build

#-------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
%defattr(-,root,root)
%{_bindir}/*
%{freemat_dir}
