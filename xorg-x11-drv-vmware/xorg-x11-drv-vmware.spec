%define debug_package %{nil}
%define tarball xf86-video-vmware
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:    Xorg X11 vmware video driver
Name:	    xorg-x11-drv-vmware
Version:    13.2.1
Release:    1
URL:	    http://www.x.org
License:    MIT

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
#git clone git://anongit.freedesktop.org/xorg/driver/xf86-video-vmware
#Source0: %{tarball}.tar.gz

ExclusiveArch: %{ix86} x86_64 ia64

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libdrm-devel pkgconfig(xext) pkgconfig(x11)
BuildRequires: mesa-libxatracker-devel >= 8.0.1-4
BuildRequires: libXfont-devel
#for libudev
BuildRequires: systemd-devel
 
Requires:  xorg-x11-server-Xorg
Requires: mesa-libxatracker >= 8.0.1-4
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 vmware video driver.

%prep
%setup -q -n %{tarball}-%{version}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%{driverdir}/vmware_drv.so
%{_mandir}/man4/vmware.4*

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 13.0.2-11.git
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 13.0.2-10.git
- Rebuild for new 4.0 release

* Sun Aug 09 2015 Cjacker <cjacker@foxmail.com>
- update to git master.
