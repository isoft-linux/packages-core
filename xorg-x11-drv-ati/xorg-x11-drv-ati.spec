%define tarball xf86-video-ati
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
Summary:   Xorg X11 ati video driver
Name:      xorg-x11-drv-ati
Version:   7.6.0
Release:   2.git
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

#Source0:    http://www.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
#git clone git://anongit.freedesktop.org/xorg/driver/xf86-video-ati
Source0: %{tarball}.tar.gz

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
%setup -q -n %{tarball}
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
* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to 3791fce
* Tue Jul 15 2015 Cjacker <cjacker@foxmail.com>
- update to lastest git codes.
