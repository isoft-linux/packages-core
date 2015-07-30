Summary: X.Org X11 libXi runtime library
Name:    libXi
Version: 1.7.4
Release: 1
License: MIT/X11
Group:  CoreGUI/Runtime/Library
URL: http://www.x.org
Source0: %{name}-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXau-devel

%description
X.Org X11 libXi runtime library

%package devel
Summary: X.Org X11 libXi development package
Group:  CoreGUI/Development/Library
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

%description devel
X.Org X11 libXi development package

%prep
%setup -q

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
%{_libdir}/libXi.so.6
%{_libdir}/libXi.so.6.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXi.so
%{_libdir}/pkgconfig/xi.pc
%{_includedir}/X11/extensions/*.h
%{_mandir}/man3/*
%{_docdir}/libXi/*.xml
