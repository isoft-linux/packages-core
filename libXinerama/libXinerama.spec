Summary: X.Org X11 libXinerama runtime library
Name: libXinerama
Version: 1.1.3
Release: 2.2
License: MIT/X11
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/releases/X11R7.0-RC4/everything/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXinerama runtime library

%package devel
Summary: X.Org X11 libXinerama development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXinerama development package

%prep
%setup -q -n libXinerama-%{version}

%build
%configure \
	--disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libXinerama.so.1
%{_libdir}/libXinerama.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXinerama.so
%{_libdir}/pkgconfig/xinerama.pc
%{_includedir}/X11/extensions/*.h
%{_mandir}/man3/*
%changelog
* Fri Oct 23 2015 cjacker - 1.1.3-2.2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

