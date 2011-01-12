# Requires llvm 2.5
%define		with_llvm			0

# Cyclic dependencies
%define		_disable_ld_no_undefined	1

%define		freemat_dir			%{_datadir}/FreeMat

Name:		freemat
Group:		Sciences/Mathematics
License:	GPL
Summary:	rapid engineering, scientific prototyping and data processing
Version:	4.0.1
Release:	%mkrel 1
URL:		http://freemat.sourceforge.net
Source0:	http://downloads.sourceforge.net/freemat/FreeMat-4.0-Source.tar.gz
Source1:	http://www.netlib.org/lapack/lapack-3.2.2.tgz
Source3:	http://www.netlib.org/clapack/CLAPACK-3.1.1/F2CLIBS/libf2c/pow_ii.c
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#-------------------------------------------------------------------------------
BuildRequires:	amd-devel
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	f2c
BuildRequires:	fftw-devel
BuildRequires:	gcc-gfortran
BuildRequires:	GL-devel
BuildRequires:	libatlas-devel
%if %{with_llvm}
BuildRequires:	llvm
%endif
BuildRequires:	pcre-devel
BuildRequires:	portaudio-devel
BuildRequires:	qt4-devel
BuildRequires:	umfpack-devel
BuildRequires:	zlib-devel

#-------------------------------------------------------------------------------
Requires:	libatlas

#-------------------------------------------------------------------------------
Patch0:		FreeMat-4.0-llvm-version.patch
Patch1:		FreeMat-4.0-constructor.patch
Patch2:		FreeMat-4.0-missing.patch
Patch3:		FreeMat-4.0-blas.patch
Patch4:		FreeMat-4.0-freemat_dir.patch
Patch5:		FreeMat-4.0-install_libs.patch

#-------------------------------------------------------------------------------
%description
FreeMat is a free environment for rapid engineering and scientific prototyping
and data processing. It is similar to commercial systems such as MATLAB from
Mathworks, and IDL from Research Systems, but is Open Source.

#-------------------------------------------------------------------------------
%prep
%setup -q -n FreeMat-%{version}-Source -a 1

# Regenerate some files to avoid build failures
rm -f CMakeCache.txt `find libs -name \*.moc.cpp` `find src -name \*.moc.cpp`

for file in `find . -name CMake\*.txt`; do dos2unix -U $file; done
%if %{with_llvm}
%patch0		-p1
%endif
%patch1		-p1

# undefined references
%patch2		-p1
cp -f %{SOURCE3} libs/libMath/libLAPACK_C
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

%patch3		-p1
perl -pi -e 's|@@FREEMAT_DIR@@|%{freemat_dir}|;'	\
	libs/libMath/libDynBlas/blas_dyn_link.cpp

%patch4		-p1

#-------------------------------------------------------------------------------
%build
export CFLAGS="`echo %{optflags} | sed 's/-O[0-9]/-O1/'` -fPIC -funsigned-char"
export CXXFLAGS="`echo %{optflags} | sed 's/-O[0-9]/-O1/'` -fPIC -funsigned-char"

(
%cmake	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}		\
%if %{with_llvm}
	-DUSE_LLVM:BOOL=ON
%else
	-DUSE_LLVM:BOOL=OFF
%endif
%make CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS"
)

#-------------------------------------------------------------------------------
%install
%makeinstall_std -C build
%makeinstall_std -C build/libs

cat > %{buildroot}%{_bindir}/freemat << EOF
#!/bin/sh

export LD_LIBRARY_PATH=%{_libdir}/FreeMat:\$LD_LIBRARY_PATH
%{freemat_dir}/FreeMat "\$@"
EOF
chmod +x  %{buildroot}/%{_bindir}/freemat
mv %{buildroot}%{_bindir}/FreeMat %{buildroot}%{freemat_dir}

#-------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/FreeMat/lib*.so
%{freemat_dir}
