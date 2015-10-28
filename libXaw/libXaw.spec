Summary: X.Org X11 libXaw runtime library
Name: libXaw
Version: 1.0.13
Release: 2
License: MIT/X11
URL: http://www.x.org

Source0: libXaw-%{version}.tar.bz2 
Patch0:  libXaw-remove-ps.patch
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: libXpm-devel
# configure doesn't complain about libXext missing, but the build fails
# without it.
BuildRequires: libXext-devel

Obsoletes: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXaw runtime library

%package devel
Summary: X.Org X11 libXaw development package
Requires: %{name} = %{version}-%{release}
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Requires: libXmu-devel

Obsoletes: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXaw development package

%prep
%setup -q

%build
%configure \
    --disable-xaw8 \
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
%{_libdir}/libXaw.so.6
%{_libdir}/libXaw.so.7
%{_libdir}/libXaw6.so.6
%{_libdir}/libXaw6.so.6.0.1
%{_libdir}/libXaw7.so.7
%{_libdir}/libXaw7.so.7.0.0

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xaw
%{_includedir}/X11/Xaw/*.h
# FIXME:  Is this C file really supposed to be here?
%{_includedir}/X11/Xaw/Template.c
%{_libdir}/libXaw.so
%{_libdir}/libXaw6.so
%{_libdir}/libXaw7.so
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/xaw6.pc
%{_libdir}/pkgconfig/xaw7.pc
#%dir %{_datadir}/aclocal
#%{_datadir}/aclocal/xaw.m4
%dir %{_mandir}/man3
%{_mandir}/man3/*.3*
%{_docdir}/libXaw/*
%changelog
* Fri Oct 23 2015 cjacker - 1.0.13-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

