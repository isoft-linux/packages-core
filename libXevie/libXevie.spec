Summary: X Event Interceptor Library
Name: libXevie
Version: 1.0.3
Release: 10%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: libX11-devel
BuildRequires: libXext-devel

%description
X Event Interceptor Library.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
libXevie development package.

%prep
%setup -q

# Disable static library creation by default.
%define with_static 0

%build
autoreconf -v --install --force
%configure \
%if ! %{with_static}
	--disable-static
%endif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXevie.so.1
%{_libdir}/libXevie.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xevie.h
%if %{with_static}
%{_libdir}/libXevie.a
%endif
%{_libdir}/libXevie.so
%{_libdir}/pkgconfig/xevie.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
