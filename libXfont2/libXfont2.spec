Summary: X.Org X11 libXfont2 runtime library
Name: libXfont2
Version: 2.0.1
Release: 3
License: MIT/X11
URL: http://www.x.org
Source0:  %{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libfontenc-devel
BuildRequires: freetype-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXfont2 runtime library

%package devel
Summary: X.Org X11 libXfont2 development package
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
%{_libdir}/libXfont2.so.2
%{_libdir}/libXfont2.so.2.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/fonts/libxfont2.h
%{_libdir}/libXfont2.so
%{_libdir}/pkgconfig/xfont2.pc

%changelog
* Tue Nov 29 2016 cjacker - 2.0.1-3
- Rebuild

* Tue Nov 29 2016 cjacker - 2.0.1-2
- New package

