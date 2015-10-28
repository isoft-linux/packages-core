Summary: X.Org X11 libXcomposite runtime library
Name: libXcomposite
Version: 0.4.4
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXcomposite-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXcomposite runtime library

%package devel
Summary: X.Org X11 libXcomposite development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXcomposite development package

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
%{_libdir}/libXcomposite.so.1
%{_libdir}/libXcomposite.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xcomposite.h
%{_libdir}/libXcomposite.so
%{_libdir}/pkgconfig/xcomposite.pc
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 0.4.4-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

