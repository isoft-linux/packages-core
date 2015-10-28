Summary: X.Org X11 libXvMC runtime library
Name: libXvMC
Version: 1.0.9
Release: 2
License: MIT/X11
URL: http://www.x.org

Source0: libXvMC-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXv-devel


Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXvMC runtime library

%package devel
Summary: X.Org X11 libXvMC development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Requires: libXv-devel, xorg-x11-proto-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXvMC development package

%prep
%setup -q 

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
%{_libdir}/libXvMC.so.*
%{_libdir}/libXvMCW.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XvMClib.h
%{_libdir}/libXvMC.so
%{_libdir}/libXvMCW.so
%{_libdir}/pkgconfig/xvmc.pc
%{_docdir}/libXvMC

%changelog
* Fri Oct 23 2015 cjacker - 1.0.9-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

