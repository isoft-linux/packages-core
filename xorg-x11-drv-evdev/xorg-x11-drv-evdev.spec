%define debug_package %{nil}

%define tarball xf86-input-evdev
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/input

%define cvsdate xxxxxxx

Summary:   Xorg X11 evdev input driver
Name:      xorg-x11-drv-evdev
Version:   2.10.0
Release:   5 
URL:       http://www.x.org
Source0:   xf86-input-evdev-%{version}.tar.bz2
License:   MIT/X11

BuildRequires: pkgconfig mtdev-devel
BuildRequires: xorg-x11-server-sdk

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: xorg-x11-server-Xorg, mtdev


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
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 2.10.0-5
- Update, rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 2.9.2-4
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

