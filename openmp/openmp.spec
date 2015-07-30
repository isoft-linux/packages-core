Name:	    openmp 
Summary:    openmp support for clang
Version:    3.6.2
Release:    1
License:   	University of llinois/NCSA Open Source License 
URL:        http://llvm.org
Group:      Core/Runtime/Library 
Source:     %{name}-%{version}.src.tar.xz
BuildRequires: clang, compiler-wrapper, cmake, ninja-build
BuildRequires: libcxx-devel

%description
The OpenMP subproject of LLVM is intended to contain all of the components required to build an executing OpenMP program that are outside the compiler itself. Support for OpenMP 3.1 in Clang is in the process of being promoted into the Clang mainline, and can be found at OpenMP/Clang. 

%package devel 
Summary: Headers and libraries for openmp. 
Group:   Core/Development/Library 
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for libcxx

%prep
%setup -q -n %{name}-%{version}.src

%Build
mkdir -p runtime/build
pushd runtime/build
#    -DCMAKE_C_FLAGS="-fnolibgcc" \
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
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/clang/`llvm-config --version`/include
pushd runtime/build
install -m0644 omp.h $RPM_BUILD_ROOT/usr/lib/clang/`llvm-config --version`/include/
install -m0755 libiomp5.so $RPM_BUILD_ROOT%{_libdir}
pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libiomp5.so libiomp.so
popd
popd

rpmclean

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
* Fri Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to 3.6.2
