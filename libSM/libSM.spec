Summary: X.Org X11 libSM runtime library
Name: libSM
Version: 1.2.2
Release: 4.1
License: MIT/X11
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libICE-devel
BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem

%description
X.Org X11 libSM runtime library

%package devel
Summary: X.Org X11 libSM development package
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Requires: %{name} = %{version}-%{release}
Requires: libICE-devel
Requires: xorg-x11-proto-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libSM development package

%prep
%setup -q

%build
%configure \
	--disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libSM.so.6
%{_libdir}/libSM.so.6.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11
%dir %{_includedir}/X11/SM
%{_includedir}/X11/SM/SM.h
%{_includedir}/X11/SM/SMlib.h
%{_includedir}/X11/SM/SMproto.h
%{_libdir}/libSM.so
%{_libdir}/pkgconfig/sm.pc
%{_docdir}/libSM/*.xml

%changelog
* Fri Oct 23 2015 cjacker - 1.2.2-4.1
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

