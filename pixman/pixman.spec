Summary:   a pixel manipulation library 
Name:      pixman 
Version:   0.32.6
Release:   1
URL:       http://cairographics.org
Source0:   http://www.cairographics.org/releases/%{name}-%{version}.tar.gz
License:   LGPL/MPL
Group:     System Environment/Libraries

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
Group: Development/Libraries
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
%configure --enable-warnings --disable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall 
rm $RPM_BUILD_ROOT%{_libdir}/*.a

rpmclean

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
#%{_datadir}/gtk-doc/*


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

