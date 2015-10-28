Summary: Direct Rendering Manager runtime library
Name: libepoxy
Version: 1.2
Release: 2
License: MIT
URL: http://github.com/anholt/libepoxy
Source0: https://github.com/anholt/libepoxy/archive/%{name}-%{version}.tar.gz

BuildRequires: pkgconfig automake autoconf libtool
BuildRequires: mesa-libGL-devel mesa-libGL-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: python

%description
A library for handling OpenGL function pointer management.

%package devel
Summary: Development files for libepoxy
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
autoreconf -ivf
%configure \
    --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT


%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libepoxy.so.*

%files devel
%dir %{_includedir}/epoxy/
%{_includedir}/epoxy/*
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.2-2
- Rebuild for new 4.0 release

