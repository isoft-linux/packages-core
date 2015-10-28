%global build_with_ninja 1 

Summary:    A standard conformant and high-performance implementation of the C++ Standard Library
Name:	    libcxx	
Version:    3.7.1
Release:    4.svn20151018 
URL:        http://llvm.org
License: University of llinois/NCSA Open Source License 

Source0:    http://llvm.org/releases/3.7.0/libcxx-%{version}.src.tar.xz
Source1:    http://llvm.org/releases/3.7.0/libcxxabi-%{version}.src.tar.xz
Source2:    http://llvm.org/releases/3.7.0/libunwind-%{version}.src.tar.xz

#it's really no need to link to gcc anymore
Patch0: libcxx-remove-libgcc.patch

BuildRequires: clang 
BuildRequires: cmake

%if %{build_with_ninja}
BuildRequires: ninja-build
%else
BuildRequires: make 
%endif

BuildRequires: libcxxabi-devel

%description
The libc++ projects provide a standard conformant and high-performance implementation of the C++ Standard Library, including full support for C++'0x

%package devel 
Summary: Headers and libraries for libcxx 
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for libcxx

%prep
%setup -q -c -a1 -a2

pushd libcxx-%{version}.src
%patch0 -p1
popd

%Build
pushd libcxx-%{version}.src
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
    -DLIBCXX_CXX_ABI=libcxxabi \
    -DLIBCXX_CXX_ABI_INCLUDE_PATHS="`pwd`/../../libcxxabi-%{version}.src/include" \
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
    -DLIBCXX_ENABLE_SHARED=ON \
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
    -DCMAKE_C_FLAGS="-fPIC -fPIE" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    -DLIBCXX_CXX_ABI=libcxxabi \
    -DLIBCXX_CXX_ABI_INCLUDE_PATHS="`pwd`/../../libcxxabi-%{version}.src/include" \
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
    -DLIBCXX_ENABLE_SHARED=OFF \
    ..

%if %{build_with_ninja}
ninja
%else
make %{_smp_mflags}
%endif
popd

popd

%install
pushd libcxx-%{version}.src
rm -rf $RPM_BUILD_ROOT

pushd build-shared
%if %{build_with_ninja}
DESTDIR=$RPM_BUILD_ROOT ninja install
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif
popd

pushd build-static
install -m0755 lib/libc++.a $RPM_BUILD_ROOT/%{_libdir}
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
%{_includedir}/c++/v1

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
