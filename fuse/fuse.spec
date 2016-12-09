Name:           fuse
Version:        2.9.7
Release:        1
Summary:        File System in Userspace (FUSE) utilities

License:        GPL+
URL:            http://fuse.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Patch1:		fuse-0001-More-parentheses.patch
Requires:       which
Conflicts:      filesystem < 3

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
License:        LGPLv2+
Conflicts:      filesystem < 3

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+
Conflicts:      filesystem < 3

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
%patch1 -p1 -b .add_parentheses

%build
export MOUNT_FUSE_PATH="%{_sbindir}"
CFLAGS="%{optflags} -D_GNU_SOURCE" %configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a
# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse

# Install config-file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

# Delete pointless udev rules, which do not belong in /etc (brc#748204)
rm -f %{buildroot}%{_sysconfdir}/udev/rules.d/99-fuse.rules

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING
%{_sbindir}/mount.fuse
%attr(4755,root,root) %{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%doc COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files devel
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
* Fri Dec 09 2016 sulit - 2.9.7-1
- upgrade fuse to 2.9.7

* Fri Oct 23 2015 cjacker - 2.9.4-11
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

