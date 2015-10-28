Summary: X.Org X11 libXdamage runtime library
Name: libXdamage
Version: 1.1.4
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXdamage-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: libX11-devel
BuildRequires: libXfixes-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXdamage runtime library

%package devel
Summary: X.Org X11 libXdamage development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXdamage development package

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
%{_libdir}/libXdamage.so.1
%{_libdir}/libXdamage.so.1.1.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xdamage.h
%{_libdir}/libXdamage.so
%{_libdir}/pkgconfig/xdamage.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.1.4-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

