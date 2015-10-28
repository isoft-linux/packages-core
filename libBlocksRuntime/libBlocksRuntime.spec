Name:       libBlocksRuntime
Summary:    Blocks Runtime library 
Version:    0.4.1
Release:    2
License:    the MIT license and the UIUC License (a BSD-like license). 
Source0:    https://github.com/mheily/blocks-runtime/releases/download/v0.4.1/libblocksruntime-%{version}.tar.gz

%description
Blocks are a proposed extension to the C, Objective C, and C++ languages developed by Apple to support the Grand Central Dispatch concurrency engine. Blocks are anonymous inline functions that automatically capture a read-only copy of local variables, and have read-write access to local variables that are declared with the "__block" storage class.

This package contains a library that is needed by programs that use Blocks.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n libblocksruntime-%{version}

%build
export CC=clang
export CFLAGS="-fPIC"
autoreconf -ivf
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install
chmod +x %{buildroot}/%{_libdir}/*.so*

install -m0755 .libs/libBlocksRuntime.a %{buildroot}/%{_libdir}

%check
make check

%clean
#[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
* Fri Oct 23 2015 cjacker - 0.4.1-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

