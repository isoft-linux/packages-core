Summary: X.Org X11 libXpm runtime library
Name: libXpm
Version: 3.5.11
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXpm-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXpm runtime library

%package devel
Summary: X.Org X11 libXpm development package

Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: libX11-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXpm development package

%prep
%setup -q -n libXpm-%{version}

%build
autoreconf -ivf
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
%{_libdir}/libXpm.so.4
%{_libdir}/libXpm.so.4.11.0

%files devel
%defattr(-,root,root,-)
%{_bindir}/cxpm
%{_bindir}/sxpm
%{_includedir}/X11/xpm.h
%{_libdir}/libXpm.so
%{_libdir}/pkgconfig/xpm.pc
%{_mandir}/man1/*.1*

%changelog
* Fri Oct 23 2015 cjacker - 3.5.11-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

