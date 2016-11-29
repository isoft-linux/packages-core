Summary: X.Org X11 libXfont runtime library
Name: libXfont
Version: 1.5.2
Release: 2
License: MIT/X11
URL: http://www.x.org
Source0:  %{name}-%{version}.tar.bz2
Patch:	libXfont-1.1.0-FreeType-2.2.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libfontenc-devel
BuildRequires: freetype-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXfont runtime library

%package devel
Summary: X.Org X11 libXfont development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
# NOTE: libXfont headers include proto headers, so this is needed.
Requires: xorg-x11-proto-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXfont development package

%prep
%setup -q -n %{name}-%{version}

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
%{_libdir}/libXfont.so.1
%{_libdir}/libXfont.so.1.4.1

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/fonts
%{_includedir}/X11/fonts/bdfint.h
%{_includedir}/X11/fonts/ft.h
%{_includedir}/X11/fonts/ftfuncs.h
%{_includedir}/X11/fonts/bitmap.h
%{_includedir}/X11/fonts/bufio.h
%{_includedir}/X11/fonts/fntfil.h
%{_includedir}/X11/fonts/fntfilio.h
%{_includedir}/X11/fonts/fntfilst.h
%{_includedir}/X11/fonts/fontconf.h
%{_includedir}/X11/fonts/fontencc.h
%{_includedir}/X11/fonts/fontmisc.h
#%{_includedir}/X11/fonts/fontmod.h
%{_includedir}/X11/fonts/fontshow.h
%{_includedir}/X11/fonts/fontutil.h
%{_includedir}/X11/fonts/fontxlfd.h
%{_includedir}/X11/fonts/pcf.h
%{_libdir}/libXfont.so
%{_libdir}/pkgconfig/xfont.pc

%changelog
* Tue Nov 29 2016 cjacker - 1.5.2-2
- Update

* Fri Oct 23 2015 cjacker - 1.5.1-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

