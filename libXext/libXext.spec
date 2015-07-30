Summary: X.Org X11 libXext runtime library
Name: libXext
Version: 1.3.3
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0: libXext-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXext runtime library

%package devel
Summary: X.Org X11 libXext development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Requires: libX11-devel
Requires: xorg-x11-proto-devel >= 7.0-1

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXext development package

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
%{_libdir}/libXext.so.6
%{_libdir}/libXext.so.6.4.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXext.so
%{_libdir}/pkgconfig/xext.pc
%{_mandir}/man3/*
%{_includedir}/X11/extensions/*.h
%{_docdir}/libXext/*.xml
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

