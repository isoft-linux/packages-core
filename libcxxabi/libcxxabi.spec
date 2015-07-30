%global build_with_ninja 1

Name:	    libcxxabi	
Summary:    A new implementation of low level support for a standard C++ library.
Version:    3.6.2
Release:    1
License:   	University of llinois/NCSA Open Source License 
Group:      Core/Runtime/Library 
URL:        http://llvm.org

Source:     %{name}-%{version}.src.tar.xz

BuildRequires: clang

%description
%{summary}

%package devel 
Summary: Headers and libraries for libcxxabi
Group:   Core/Development/Library 
Requires: %{name} = %{version}-%{release}

%description devel 
Headers and libbraries for libcxxabi

%prep
%setup -q -n %{name}-%{version}.src

%build
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
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -fPIC -fPIE" \
    -DCMAKE_SHARED_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_MODULE_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_EXE_LINKER_FLAGS="-pie -nodefaultlibs" \
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
    -DCMAKE_C_FLAGS="-fPIC -fPIE" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -fPIC -fPIE" \
    -DCMAKE_SHARED_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_MODULE_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DCMAKE_EXE_LINKER_FLAGS="-pie -nodefaultlibs" \
    -DLIBCXXABI_ENABLE_SHARED=OFF \
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
%if %{build_with_ninja}
DESTDIR=$RPM_BUILD_ROOT ninja install
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif
popd


#install headers of libcxxabi for compile libcxx with it.
mkdir -p %{buildroot}%{_includedir}/libcxxabi 
cp -r include/* %{buildroot}%{_includedir}/libcxxabi

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
%{_includedir}/libcxxabi

%changelog
* Fri Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to 3.6.2
