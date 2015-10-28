%global build_with_ninja 1

Name:	    libcxxabi	
Summary:    A new implementation of low level support for a standard C++ library.
Version:    3.7.1
Release:    4.svn20151018
License:  University of llinois/NCSA Open Source License 
URL:        http://llvm.org

Source0:    http://llvm.org/releases/3.7.0/libcxxabi-%{version}.src.tar.xz
Source1:    http://llvm.org/releases/3.7.0/libunwind-%{version}.src.tar.xz
Source2:    http://llvm.org/releases/3.7.0/libcxx-%{version}.src.tar.xz

BuildRequires: clang cmake

%if %{build_with_ninja}
BuildRequires: ninja-build
%else 
BuildRequires: make
%endif

BuildRequires: libunwind-devel

%description
%{summary}

%package devel 
Summary: Headers and libraries for libcxxabi
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for libcxxabi

%prep
%setup -q -c -a1 -a2

%build
pushd %{name}-%{version}.src
#build shared library
mkdir build-shared
pushd build-shared
%cmake \
    %if %{build_with_ninja}
    -G Ninja \
    %endif
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++  \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
    -DLIBCXXABI_LIBUNWIND_PATH="`pwd`/../../libunwind-%{version}.src" \
    -DLIBCXXABI_LIBCXX_INCLUDES="`pwd`/../../libcxx-%{version}.src/include" \
    -DLIBCXXABI_ENABLE_SHARED=ON \
    ..

%if %{build_with_ninja}
ninja
%else
make %{_smp_mflags}
%endif
popd

#build static library
mkdir build-static
pushd build-static
%cmake \
    %if %{build_with_ninja}
    -G Ninja \
    %endif
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++  \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
    -DLIBCXXABI_LIBUNWIND_PATH="`pwd`/../../libunwind-%{version}.src" \
    -DLIBCXXABI_LIBCXX_INCLUDES="`pwd`/../../libcxx-%{version}.src/include" \
    -DLIBCXXABI_ENABLE_SHARED=OFF \
    ..

%if %{build_with_ninja}
ninja
%else
make %{_smp_mflags}
%endif
popd

popd


%install
pushd %{name}-%{version}.src

rm -rf $RPM_BUILD_ROOT
pushd build-shared
%if %{build_with_ninja}
DESTDIR=$RPM_BUILD_ROOT ninja install
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif
popd

pushd build-static
%if %{build_with_ninja}
DESTDIR=$RPM_BUILD_ROOT ninja install
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif
popd


popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
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
