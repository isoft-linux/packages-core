Summary: X.Org X11 libICE runtime library
Name: libICE
Version: 1.0.9
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0:%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem


%description
X.Org X11 libICE runtime library

%package devel
Summary: X.Org X11 libICE development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libICE development package

%prep
%setup -q 

%build
%configure \
       --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libICE.so.6
%{_libdir}/libICE.so.6.3.0

%files devel
%dir %{_includedir}/X11
%dir %{_includedir}/X11/ICE
%{_includedir}/X11/ICE/ICE.h
%{_includedir}/X11/ICE/ICEconn.h
%{_includedir}/X11/ICE/ICElib.h
%{_includedir}/X11/ICE/ICEmsg.h
%{_includedir}/X11/ICE/ICEproto.h
%{_includedir}/X11/ICE/ICEutil.h
%{_libdir}/libICE.so
%{_libdir}/pkgconfig/ice.pc
%{_docdir}/libICE/*.xml

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

