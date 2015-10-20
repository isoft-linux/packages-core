Summary: X.Org X11 libX11 runtime library
Name:    libX11
Version: 1.6.3
Release: 7 
License: MIT/X11
Group:   CoreGUI/Runtime/Library
URL:     http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

#this patch is important to support cusror follow in openjdk awt/swing apps.
#Please be careful when update!!!!!

#By cjacker.
Patch0: libX11-pass_XNSpotLocation_info_for_most_preedit_styles.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libxcb-devel
Requires:      libxcb

Requires(pre): xorg-x11-filesystem >= 0.99.2-3

%description
X.Org X11 libX11 runtime library

%package devel
Summary: X.Org X11 libX11 development package
Group:   CoreGUI/Development/Library
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: %{name} = %{version}-%{release}

Requires: xorg-x11-proto-devel >= 7.1-2
Requires: libXau-devel, libXdmcp-devel, libxcb-devel

%description devel
X.Org X11 libX11 development package

%prep
%setup -q 
%patch0 -p1

%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#remove useless file.
rm -rf $RPM_BUILD_ROOT%{_datadir}/X11/Xcms.txt 

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_datadir}/X11
%{_datadir}/X11/XErrorDB
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_libdir}/libX11.so.*
%{_libdir}/libX11-xcb.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11
%{_includedir}/X11/*.h
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_datadir}/doc/libX11

%changelog
* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com>
- rebuild.
