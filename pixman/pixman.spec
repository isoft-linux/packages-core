Summary:   a pixel manipulation library 
Name:      pixman 
Version:   0.33.4
Release:   3 
License:   LGPL/MPL
URL:       http://cairographics.org
Source0:   http://www.cairographics.org/releases/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
Requires(post): /sbin/ldconfig

%description 
pixman is a library that provides low-level pixel manipulation
features such as image compositing and trapezoid rasterization.

%package devel
Summary: pixman developmental libraries and header files
Requires: %{name} = %{version}-%{release}
Requires: libpng-devel
Requires: freetype-devel
Requires: fontconfig-devel

%description devel
Developmental libraries and header files required for developing or
compiling software which links to the pixman library

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall 
rm $RPM_BUILD_ROOT%{_libdir}/*.a


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libpixman*.so.* 

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libpixman*.so
%{_libdir}/pkgconfig/*


%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 0.33.4-3
- Update

* Fri Oct 23 2015 cjacker - 0.32.8-2
- Rebuild for new 4.0 release

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 0.32.8

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

