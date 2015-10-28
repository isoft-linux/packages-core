Summary: X.Org X11 libXdmcp runtime library
Name: libXdmcp
Version: 1.1.2
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXdmcp-%{version}.tar.bz2 

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel

BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem
%description
X.Org X11 libXdmcp runtime library

%package devel
Summary: X.Org X11 libXdmcp development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXdmcp development package

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
%{_libdir}/libXdmcp.so.6
%{_libdir}/libXdmcp.so.6.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/Xdmcp.h
%{_libdir}/libXdmcp.so
%{_libdir}/pkgconfig/xdmcp.pc
%{_docdir}/libXdmcp/*.xml


%changelog
* Fri Oct 23 2015 cjacker - 1.1.2-2
- Rebuild for new 4.0 release

