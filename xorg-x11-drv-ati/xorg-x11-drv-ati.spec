%define debug_package %{nil}
%define tarball xf86-video-ati
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
Summary:   Xorg X11 ati video driver
Name:      xorg-x11-drv-ati
Version:   7.8.0
Release:   2
URL:       http://www.x.org
License:   MIT

Source0:    http://www.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2

Patch10:    radeon-6.12.2-lvds-default-modes.patch
Patch13:    fix-default-modes.patch

ExcludeArch: s390 s390x

BuildRequires: python
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.4.33-1
BuildRequires: kernel-headers >= 2.6.27-0.308
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: libudev-devel
BuildRequires: xorg-x11-server-devel

Requires:  xorg-x11-server-Xorg
Requires: libdrm >= 2.4.36-1

%description 
X.Org X11 ati video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch10 -p1 -b .lvds
%patch13 -p1 -b .def

%build
if [ ! -f "configure" ]; then autoreconf -ivf; fi
%configure --disable-static --enable-glamor
make %{?_smp_mflags}

%install
%make_install

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# these only work in UMS, which is not supported
rm -rf $RPM_BUILD_ROOT%{moduledir}/multimedia/

%files
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*

%changelog
* Tue Nov 29 2016 cjacker - 7.8.0-2
- Update

* Fri Dec 04 2015 sulit <sulitsrc@gmail.com> - 7.6.0-11.git
- update to git codes 78fbca0
- Load fb module before glamoregl/shadow modules

* Tue Dec 01 2015 sulit <sulitsrc@gmail.com> - 7.6.0-10.git
- minor modifictions, update to git codes b19417e
- Don't advertise any PRIME offloading capabilities without acceleration

* Mon Nov 23 2015 Cjacker <cjacker@foxmail.com> - 7.6.0-9.git
- Rebuild with xorg server

* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 7.6.0-8.git
- Update to 10b7c3d

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 7.6.0-7.git
- Rebuild with xorg-server 1.8.0

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 7.6.0-6.git
- git 7186a87

* Fri Oct 23 2015 cjacker - 7.6.0-5.git
- Rebuild for new 4.0 release

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 7.6.0-4.git
- Update to 548e97b,fix rotation issue

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to 3791fce

* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- update to lastest git codes.
