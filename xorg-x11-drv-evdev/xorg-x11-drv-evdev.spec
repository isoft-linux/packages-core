%define tarball xf86-input-evdev
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/input

%define cvsdate xxxxxxx

Summary:   Xorg X11 evdev input driver
Name:      xorg-x11-drv-evdev
Version:   2.9.2
Release:    3 
URL:       http://www.x.org
Source0:   xf86-input-evdev-%{version}.tar.bz2
License:   MIT/X11
Group:     User Interface/X Hardware Support

BuildRequires: pkgconfig mtdev-devel
BuildRequires: xorg-x11-server-sdk

Requires:  xorg-x11-server-Xorg, mtdev


%description 
X.Org X11 evdev input driver.

%package devel
Summary:  Xorg X11 evdev input driver development package.
Requires: pkgconfig

%description devel
Xorg X11 evdev input driver development files.

%prep
%setup -q -n xf86-input-evdev-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{moduledir}
%dir %{driverdir}
%{driverdir}/evdev_drv.so
%{_mandir}/man4/evdev.4*

%files devel
%{_includedir}/xorg/evdev-properties.h
%{_libdir}/pkgconfig/xorg-evdev.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

