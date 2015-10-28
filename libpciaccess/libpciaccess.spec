Name:           libpciaccess
Version:        0.13.4
Release:        3
Summary:        PCI access library

License:        MIT
URL:            http://cgit.freedesktop.org/xorg/lib/libpciaccess/
Source0:	    http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig
Requires:       hwdata

%description
libpciaccess is a library for portable PCI access routines across multiple
operating systems.

%package devel
Summary:        PCI access library development package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development package for libpciaccess.

%prep
%setup -q -n %{name}-%{version}
%build

! [ -f ./configure ] && ./autogen.sh
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS ChangeLog
%{_libdir}/libpciaccess.so.0
%{_libdir}/libpciaccess.so.0.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/pciaccess.h
%{_libdir}/libpciaccess.so
%{_libdir}/pkgconfig/pciaccess.pc

%changelog
* Fri Oct 23 2015 cjacker - 0.13.4-3
- Rebuild for new 4.0 release

* Thu Nov 14 2013 Cjacker <cjacker@gmail.com>
- prepare for a new dist.
