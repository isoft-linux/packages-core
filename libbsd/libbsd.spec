Name:		libbsd
Version:	0.7.0
Release:	4
Summary:	Library providing BSD-compatible functions for portability
URL:		http://libbsd.freedesktop.org/
License:	BSD and ISC and Copyright only and Public Domain
Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package devel
Summary:	Development files for libbsd
Requires:	libbsd = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development files for the libbsd library.

%package ctor-static
Summary:	Development files for libbsd
Requires:	libbsd = %{version}-%{release}
Requires:	pkgconfig

%description ctor-static
The libbsd-ctor static library is required if setproctitle() is to be used
when libbsd is loaded via dlopen() from a threaded program.  This can be
configured using "pkg-config --libs libbsd-ctor".

%prep
%setup -q

%configure

%build
make CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
rm -rf %{buildroot}   # necessary for EL5 only
make libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot} \
     install

# don't want static library or libtool archive
rm %{buildroot}%{_libdir}/%{name}.a
rm %{buildroot}%{_libdir}/%{name}.la


%check
make check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/%{name}.so.*

%files devel
%{_mandir}/man3/*.3.gz
%{_mandir}/man3/*.3bsd.gz
%{_includedir}/bsd
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-overlay.pc

%files ctor-static
%{_libdir}/%{name}-ctor.a
%{_libdir}/pkgconfig/%{name}-ctor.pc

%changelog
* Fri Oct 23 2015 cjacker - 0.7.0-4
- Rebuild for new 4.0 release

