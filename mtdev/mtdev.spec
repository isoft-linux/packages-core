Name:           mtdev
Version:        1.1.5
Release:        2
Summary:        Multitouch Protocol Translation Library

License:        MIT
URL:            http://bitmath.org/code/mtdev/

Source0:        http://bitmath.org/code/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf automake libtool

%description
%{name} is a stand-alone library which transforms all variants of kernel MT
events to the slotted type B protocol. The events put into mtdev may be from
any MT device, specifically type A without contact tracking, type A with
contact tracking, or type B with contact tracking.

%package devel
Summary:        Multitouch Protocol Translation Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Multitouch protocol translation library development package.

%prep
%setup -q

%build
autoreconf --force -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libmtdev.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mtdev.h
%{_includedir}/mtdev-plumbing.h
%{_includedir}/mtdev-mapping.h
%{_libdir}/libmtdev.so
%{_libdir}/pkgconfig/mtdev.pc
%{_bindir}/mtdev-test

%changelog
* Fri Oct 23 2015 cjacker - 1.1.5-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

