Summary: X.Org X11 libXt runtime library
Name: libXt
Version: 1.1.5
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0: libXt-%{version}.tar.bz2 

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libSM-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXt runtime library

%package devel
Summary: X.Org X11 libXt development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: libX11-devel
Requires: libSM-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXt development package

%prep
%setup -q -n libXt-%{version}

%build
%configure \
	--disable-static \
	--with-xfile-search-path="%{_sysconfdir}/X11/%%L/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%l/%%T/\%%N%%C%%S:%{_sysconfdir}/X11/%%T/%%N%%C%%S:%{_sysconfdir}/X11/%%L/%%T/%%N%%S:%{_sysconfdir}/X\11/%%l/%%T/%%N%%S:%{_sysconfdir}/X11/%%T/%%N%%S:%{_datadir}/X11/%%L/%%T/%%N%%C%%S:%{_datadir}/X1\1/%%l/%%T/%%N%%C%%S:%{_datadir}/X11/%%T/%%N%%C%%S:%{_datadir}/X11/%%L/%%T/%%N%%S:%{_datadir}/X11/%%\l/%%T/%%N%%S:%{_datadir}/X11/%%T/%%N%%S"

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
%{_libdir}/libXt.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/*.h
%{_libdir}/libXt.so
%{_libdir}/pkgconfig/xt.pc
%{_mandir}/man3/*.3*
%{_docdir}/libXt/*.xml

%changelog
* Fri Oct 23 2015 cjacker - 1.1.5-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

