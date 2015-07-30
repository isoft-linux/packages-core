Summary: X.Org X11 libXcursor runtime library
Name: libXcursor
Version: 1.1.14
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0: libXcursor-%{version}.tar.bz2 
Source1: index.theme

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrender-devel >= 0.8.2

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXcursor runtime library

%package devel
Summary: X.Org X11 libXcursor development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXcursor development package

%prep
%setup -q -n libXcursor-%{version}

%build
%configure \
	--disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/default
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/icons/default/index.theme

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libXcursor.so.1
%{_libdir}/libXcursor.so.1.0.2
%dir %{_datadir}/icons/default
%config(noreplace) %verify(not md5 size mtime) %{_datadir}/icons/default/index.theme

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%{_libdir}/libXcursor.so
%{_libdir}/pkgconfig/xcursor.pc
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

