Summary: X.Org X11 libXtst runtime library
Name: libXtst
Version: 1.2.3
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/X11R7.0/src/everything/%{name}-%{version}.tar.bz2

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXi-devel
Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXtst runtime library

%package devel
Summary: X.Org X11 libXtst development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXtst development package

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
%{_libdir}/libXtst.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXtst.so
%{_libdir}/pkgconfig/xtst.pc
%{_includedir}/X11/extensions/*
%{_mandir}/man3/*
%{_docdir}/libXtst

%changelog
* Tue Nov 29 2016 cjacker - 1.2.3-2
- Update

* Fri Oct 23 2015 cjacker - 1.2.2-2.2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

