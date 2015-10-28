Summary: X.Org X11 application bitmaps for development usage
Name: xbitmaps-devel 
Version: 1.1.1
Release: 4
License: MIT/X11
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/releases/individual/data/xbitmaps-%{version}.tar.bz2 
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Provides: xbitmaps
Provides: xbitmaps-devel
Provides: xorg-x11-xbitmaps

BuildArch: noarch
%description
X.Org X11 application bitmaps for development usage

%prep
%setup -q -n xbitmaps-%{version}

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_includedir}/X11/bitmaps
%{_includedir}/X11/bitmaps/*
%{_datadir}/pkgconfig/xbitmaps.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.1.1-4
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.
