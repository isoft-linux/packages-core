Summary: X.Org X11 libXrender runtime library
Name: libXrender
Version: 0.9.10
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXrender-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXrender runtime library

%package devel
Summary: X.Org X11 libXrender development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Requires: xorg-x11-proto-devel
Requires: libX11-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXrender development package

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
%{_libdir}/libXrender.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xrender.h
%{_libdir}/libXrender.so
%{_libdir}/pkgconfig/xrender.pc
%{_docdir}/libXrender

%changelog
* Tue Nov 29 2016 cjacker - 0.9.10-2
- Update

* Fri Oct 23 2015 cjacker - 0.9.9-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

