Name:       libdispatch 
Summary:    user space implementation of the Grand Central Dispatch API 
Version:    197
Release:    1
License:    Apache License, Version 2.0 
Group:      System Environment/Libraries
Url:        https://github.com/mheily/opengcd/releases
Source0:    https://github.com/mheily/opengcd/archive/REL_0_2.tar.gz

BuildRequires: libBlocksRuntime-devel
BuildRequires: libkqueue-devel

%description
The libdispatch project consists of the user space implementation of the Grand Central Dispatch API as seen in Mac OS X version 10.6 (Snow Leopard).

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n opengcd-REL_0_2

%build
pushd libdispatch-197
export CC=clang
export CXX="clang++ -stdlib=libc++"
autoreconf -ivf
%configure
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd libdispatch-197
make DESTDIR=%{buildroot} install
popd

%check
pushd libdispatch-197
make check
popd

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%dir %{_includedir}/dispatch
%{_includedir}/dispatch/*
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

