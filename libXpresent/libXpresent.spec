Summary: X.Org X11 libXpresent runtime library
Name: libXpresent
Version: 1.0.0
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXpresent-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXpm runtime library

%package devel
Summary: X.Org X11 %{name} development package

Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: libX11-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 %{name} development package

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
%{_libdir}/libXpresent.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xpresent.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 1.0.0-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

