#for bootstrap build:
#1. build libcxx without libcxxabi support, install it.
#2. build libcxxabi
#3. rebuild libcxx, enable libcxxabi support.

#how to build a libunwind/libcxxabi/libcxx/clang toolchain without dependency on libgcc/libstdc++:
#0. build llvm/clang, apply some patches. refer to the spec of llvm.
#1. build libcxx with bootstrap to 1 and rebuild_drop_libgcc to 0.
#   it will link to libgcc/libstdc++.
#2. build libcxxabi with linker option: -nodefaultlibs.
#   it will not link to any c++ library.
#   also it will not link to libgcc.
#3. build libunwind and install it. it equals to libgcc.

#4. rebuild libcxx with boostrap to 0 and rebuild_drop_libgcc to 1 
#   the patch will remove link to libgcc.
#   the CMAKE defines "-DLIBCXX_CXX_ABI=libcxxabi" will use libcxxabi instead of stdc++ as libcxx's cxxabi
#   "-fnolibgcc" is our patch to llvm/clang, with this flag, it will use libunwind instead of libgcc.
#   "-nodefaultlibs" will drop linkage to libstdc++/libc++(self link to self), it's really no need to link to a c++ library, such as libstdc++.

#NOTE:  before finished, you will find "ldd *.so" will still show depending on libgcc/libstdc++, that's implict dependencies.
%global bootstrap 0 

%global rebuild_drop_libgcc 1

%global build_with_ninja 1 


Summary:A standard conformant and high-performance implementation of the C++ Standard Library
Name:	    libcxx	
Version:    3.6.2
Release:    1
URL:        http://llvm.org
Group:      Core/Runtime/Library

Source0:     %{name}-%{version}.src.tar.xz

Patch0:     libcxx-remove-libgcc.patch

License:   	University of llinois/NCSA Open Source License 

BuildRequires: clang 
BuildRequires: cmake

%if %{build_with_ninja}
BuildRequires: ninja-build
%endif

%if !%{bootstrap}
#for cxxabi.h
BuildRequires: libcxxabi-devel
%endif

%description
The libc++ projects provide a standard conformant and high-performance implementation of the C++ Standard Library, including full support for C++'0x

%package devel 
Summary: Headers and libraries for libcxx 
Group:  Core/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for libcxx

%prep
%setup -q -n %{name}-%{version}.src
%if %{rebuild_drop_libgcc}
%patch0 -p1
%endif

%Build
#build shared library
mkdir build-shared
pushd build-shared
%cmake \
    %if %{build_with_ninja}
    -G Ninja \
    %endif
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++  \
    -DCMAKE_C_FLAGS="-fPIC -fPIE" \
    %if !%{rebuild_drop_libgcc}
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC -fPIE" \
    %else
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -lc++abi -fnolibgcc -fPIC -fPIE" \
    -DCMAKE_SHARED_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_MODULE_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_EXE_LINKER_FLAGS="-pie -nodefaultlibs" \
    %endif
    %if !%{bootstrap}
    -DLIBCXX_CXX_ABI=libcxxabi \
    -DLIBCXX_LIBCXXABI_INCLUDE_PATHS="/usr/include/libcxxabi" \
    %endif
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
    %if !%{rebuild_drop_libgcc}
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC -fPIE" \
    %else
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -lc++abi -fnolibgcc -fPIC -fPIE" \
    -DCMAKE_SHARED_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_MODULE_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_EXE_LINKER_FLAGS="-pie -nodefaultlibs" \
    %endif
    %if !%{bootstrap}
    -DLIBCXX_CXX_ABI=libcxxabi \
    -DLIBCXX_LIBCXXABI_INCLUDE_PATHS="/usr/include/libcxxabi" \
    %endif
    -DLIBCXX_ENABLE_SHARED=OFF \
    ..

%if %{build_with_ninja}
ninja
%else
make %{_smp_mflags}
%endif
popd


%install
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
rpmclean

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
* Fri Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to 3.6.2
