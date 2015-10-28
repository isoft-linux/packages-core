Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.3.2
Release: 3
License: MIT/X11
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXrender-devel
BuildRequires: freetype-devel >= 2.1.9-2
BuildRequires: fontconfig-devel >= 2.2-1

Requires: fontconfig >= 2.2-1

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXft runtime library

%package devel
Summary: X.Org X11 libXft development package
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: %{name} = %{version}-%{release}

Requires: xorg-x11-proto-devel
Requires: libXrender-devel
Requires: fontconfig-devel >= 2.2-1
Requires: freetype-devel >= 2.1.9-2

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXft development package

%prep
%setup -q

%build
%configure \
	--disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: There's no real good reason to ship these anymore, as pkg-config
# is the official way to detect flags, etc. now.
rm -f $RPM_BUILD_ROOT%{_bindir}/xft-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xft-config*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libXft.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/libXft.so
%{_libdir}/pkgconfig/xft.pc
%{_mandir}/man3/Xft.3*

%changelog
* Fri Oct 23 2015 cjacker - 2.3.2-3
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

