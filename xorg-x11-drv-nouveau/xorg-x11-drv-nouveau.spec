%define debug_package %{nil}
%define tarball xf86-video-nouveau
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 nouveau video driver(s)
Name:      xorg-x11-drv-nouveau
Version:   1.0.13
Release:   2
URL:       http://www.x.org
License:   MIT

#Source0:   %{tarball}-%{version}.tar.bz2
Source0:   http://xorg.freedesktop.org/archive/individual/driver/%{tarball}-%{version}.tar.bz2
#git://anongit.freedesktop.org/nouveau/xf86-video-nouveau
#Source0: %{tarball}-6e6d8ac.tar.xz
Patch0: fix-glamor-build.patch

BuildRequires: pkgconfig
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.3.0
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: xcb-util
Requires:  xorg-x11-server-Xorg >= 1.1.0-1
Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 nouveau video driver.

%prep
#%setup -q -n xf86-video-nouveau
%setup -q -n %{tarball}-%{version}
#%patch0 -p1

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT || exit 1

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/*.so
%{_mandir}/man4/nouveau.4*

%changelog
* Tue Nov 29 2016 cjacker - 1.0.13-2
- Update

* Mon Dec 28 2015 sulit <sulitsrc@gmail.com> - 1.0.12-1.git
- update to 1.0.12

* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 1.0.11-7.git
- Update to 6e6d8ac

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.0.11-6.git
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 1.0.11-5.git
- Rebuild for new 4.0 release

* Fri Sep 04 2015 Cjacker <cjacker@foxmail.com>
- add patch1, should fix build with xorg-server 1.8rc1, althouth we did not update yet.
* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to git master.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

