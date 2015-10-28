Summary: X.Org X11 libXss runtime library
Name: libXScrnSaver
Version: 1.2.2
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXScrnSaver-%{version}.tar.bz2 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXss runtime library

%package devel
Summary: X.Org X11 libXScrnSaver development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Requires:  libX11-devel
Requires:  libXext-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXss development package

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
%{_libdir}/libXss.so.1
%{_libdir}/libXss.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXss.so
%{_libdir}/pkgconfig/xscrnsaver.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/scrnsaver.h

%changelog
* Fri Oct 23 2015 cjacker - 1.2.2-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

