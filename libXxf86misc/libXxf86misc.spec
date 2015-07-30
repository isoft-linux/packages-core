Summary: X.Org X11 libXxf86misc runtime library
Name: libXxf86misc
Version: 1.0.3
Release: 7
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(xproto) pkgconfig(xext)

%description
X.Org X11 libXxf86misc runtime library

%package devel
Summary: X.Org X11 libXxf86misc development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXxf86misc development package

%prep
%setup -q

%build
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rpmclean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libXxf86misc.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXxf86misc.so
%{_libdir}/pkgconfig/xxf86misc.pc
%{_mandir}/man3/*.3*

%changelog
