Summary: A mouse server for the Linux console
Name: gpm
Version: 1.20.7
Release: 1
License: GPLv2+
URL: http://www.nico.schottelius.org/software/gpm/
Source: http://www.nico.schottelius.org/software/gpm/archives/%{name}-%{version}.tar.lzma
Source1: gpm.service
Patch1: gpm-1.20.6-multilib.patch
Patch2: gpm-1.20.1-lib-silent.patch
Patch4: gpm-1.20.5-close-fds.patch
Patch5: gpm-1.20.1-weak-wgetch.patch
Patch7: gpm-1.20.7-rhbz-668480-gpm-types-7-manpage-fixes.patch
Patch8: gpm-1.20.6-missing-header-dir-in-make-depend.patch
Patch9: gpm-format-security.patch

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# this defines the library version that this package builds.
%define LIBVER 2.1.0
BuildRequires: sed gawk bison ncurses-devel autoconf automake libtool texinfo libcap-ng-devel
Requires: %{name}-libs = %{version}-%{release}

%description
Gpm provides mouse support to text-based Linux applications like the
Emacs editor and the Midnight Commander file management system.  Gpm
also provides console cut-and-paste operations using the mouse and
includes a program to allow pop-up menus to appear at the click of a
mouse button.

%package libs
Summary: Dynamic library for for the gpm

%description libs
This package contains the libgpm.so dynamic library which contains
the gpm system calls and library functions.

%package devel
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Summary: Development files for the gpm library

%description devel
The gpm-devel package includes header files and libraries necessary
for developing programs which use the gpm library. The gpm provides
mouse support to text-based Linux applications.

%package static
Requires: %{name} = %{version}-%{release}
Summary: Static development files for the gpm library

%description static
The gpm-static package includes static libraries of gpm. The gpm provides
mouse support to text-based Linux applications.


%prep
%setup -q

./autogen.sh

%patch1 -p1 -b .multilib
%patch2 -p1 -b .lib-silent
%patch4 -p1 -b .close-fds
%patch5 -p1 -b .weak-wgetch
%patch7 -p1
%patch8 -p1
%patch9 -p1


%build
LDFLAGS='-Wl,-z,relro -Wl,-z,bind_now'
%configure
make %{?_smp_mflags}

%install
%make_install

chmod 0755 %{buildroot}/%{_libdir}/libgpm.so.%{LIBVER}
ln -sf libgpm.so.%{LIBVER} %{buildroot}/%{_libdir}/libgpm.so

rm -f %{buildroot}%{_datadir}/emacs/site-lisp/t-mouse.el

%ifnarch s390 s390x
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -m 644 conf/gpm-* %{buildroot}%{_sysconfdir}
# Systemd
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system
rm -rf %{buildroot}%{_initrddir}
%else
# we're shipping only libraries in s390[x], so
# remove stuff from the buildroot that we aren't shipping
rm -rf %{buildroot}%{_sbindir}
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_mandir}
%endif

%post
%ifnarch s390 s390x
%systemd_post gpm.service
%endif

%ifnarch s390 s390x
%triggerun -- gpm < 1.20.6-15
/bin/systemctl enable gpm.service >/dev/null 2>&1 || :
%endif

%preun
%ifnarch s390 s390x
%systemd_preun gpm.service
%endif

%postun
%ifnarch s390 s390x
%systemd_postun_with_restart gpm.service
%endif


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc COPYING README TODO
%doc doc/README* doc/FAQ doc/Announce doc/changelog
%ifnarch s390 s390x
%config(noreplace) %{_sysconfdir}/gpm-*
/usr/lib/systemd/system/gpm.service
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man?/*
%{_infodir}/gpm.info.gz
%endif

%files libs
%{_libdir}/libgpm.so.*

%files devel
%{_includedir}/*
%{_libdir}/libgpm.so

%files static
%{_libdir}/libgpm.a

%changelog
* Thu Dec 15 2016 sulit - 1.20.7-1
- upgrade gpm to 1.20.7

* Fri Oct 23 2015 cjacker - 1.20.6-2
- Rebuild for new 4.0 release

