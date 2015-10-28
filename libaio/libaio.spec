Name: libaio
Version: 0.3.110
Release: 6 
Summary: Linux-native asynchronous I/O access library
License: LGPLv2+
URL:    http://lse.sourceforge.net/io/aio.html
Source: http://ftp.de.debian.org/debian/pool/main/liba/libaio/libaio_%{version}.orig.tar.gz
Patch1: libaio-install-to-slash.patch

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%define libdir /%{_lib}
%define usrlibdir %{_prefix}/%{_lib}

%package devel
Summary: Development files for Linux-native asynchronous I/O access
Requires: libaio

%description devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
%setup
%patch1 -p1

%build
make CC=gcc

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make destdir=$RPM_BUILD_ROOT prefix=/ libdir=%{usrlibdir} usrlibdir=%{usrlibdir} \
	includedir=%{_includedir} install


%check
#make check CC=gcc


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,root,root) %{usrlibdir}/libaio.so.*

%files devel
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{usrlibdir}/libaio.so
%attr(0644,root,root) %{usrlibdir}/libaio.a

%changelog
* Fri Oct 23 2015 cjacker - 0.3.110-6
- Rebuild for new 4.0 release

