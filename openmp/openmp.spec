Name:	    openmp 
Summary:    openmp support for clang
Version:    3.7.1
Release:    12.254869.svn
License:    University of Illinois/NCSA Open Source License 
URL:        http://llvm.org
Source:     http://llvm.org/releases/3.7.0/openmp-%{version}.src.tar.xz
BuildRequires: clang, compiler-wrapper, cmake, ninja-build
BuildRequires: libcxx-devel libcxxabi-devel

#for llvm-config
BuildRequires: llvm-devel

%description
The OpenMP subproject of LLVM is intended to contain all of the components required to build an executing OpenMP program that are outside the compiler itself. Support for OpenMP 3.1 in Clang is in the process of being promoted into the Clang mainline, and can be found at OpenMP/Clang. 

%package devel 
Summary: Headers and libraries for openmp. 
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for openmp 

%prep
%setup -q -n %{name}-%{version}.src

%Build
mkdir -p runtime/build
pushd runtime/build
%cmake \
    -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_CXX_FLAGS="-stdlib=libc++" \
    .. 
ninja
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd runtime/build
DESTDIR=$RPM_BUILD_ROOT ninja install
popd

#avoid conflicts with gcc.
rm -rf %{buildroot}%{_libdir}/libgomp.so

#install omp.h to private path.
mkdir -p %{buildroot}%{_libdir}/clang/`llvm-config --version`/include
mv %{buildroot}%{_includedir}/omp.h %{buildroot}%{_libdir}/clang/`llvm-config --version`/include/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so

%files devel
%defattr(-,root,root)
%{_libdir}/clang/*/include/*.h

%changelog
* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-12.254869.svn
- Fix description

* Sun Dec 06 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-11.254869.svn
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-4.svn20151018
- Rebuild

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.1svn
- build with llvm-3.7.1svn

* Wed Sep 02 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.0

* Sat Jul 25 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.0rc1

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.6.2
