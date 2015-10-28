Summary: X.Org X11 libXmu/libXmuu runtime libraries
Name: libXmu
Version: 1.1.2
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXmu-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libXau-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXmu/libXmuu runtime libraries

%package devel
Summary: X.Org X11 libXmu development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXmu development package

%prep
%setup -q 

%build
#export CFLAGS="-D_DEFAULT_SOURCE"
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
%{_libdir}/libXmu.so.6
%{_libdir}/libXmu.so.6.2.0
%{_libdir}/libXmuu.so.1
%{_libdir}/libXmuu.so.1.0.0

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xmu
%{_includedir}/X11/Xmu/*
%{_libdir}/libXmu.so
%{_libdir}/libXmuu.so
%{_libdir}/pkgconfig/xmu.pc
%{_libdir}/pkgconfig/xmuu.pc
%{_docdir}/libXmu/*

%changelog
* Fri Oct 23 2015 cjacker - 1.1.2-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

