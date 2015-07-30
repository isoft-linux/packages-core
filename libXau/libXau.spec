Summary: X.Org X11 libXau runtime library
Name: libXau
Version: 1.0.8
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0: libXau-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel

BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem

%description
X.Org X11 libXau runtime library

%package devel
Summary: X.Org X11 libXau development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXau development package

%prep
%setup -q -n libXau-%{version}

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
%{_libdir}/libXau.so.6
%{_libdir}/libXau.so.6.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/Xauth.h
%{_libdir}/libXau.so
%{_libdir}/pkgconfig/xau.pc
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

