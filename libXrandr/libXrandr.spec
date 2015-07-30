Summary: X.Org X11 libXrandr runtime library
Name: libXrandr
Version: 1.5.0
Release: 2 
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0: libXrandr-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXrender-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXrandr runtime library

%package devel
Summary: X.Org X11 libXrandr development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXrandr development package

%prep
%setup -q -n libXrandr-%{version}

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
%{_libdir}/libXrandr.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xrandr.h
%{_libdir}/libXrandr.so
%{_libdir}/pkgconfig/xrandr.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

