%define debug_package %{nil}
%define tarball xf86-video-nouveau
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 nouveau video driver(s)
Name:      xorg-x11-drv-nouveau
Version:   1.0.11
Release:   5.git 
URL:       http://www.x.org
License:   MIT

#Source0:   %{tarball}-%{version}.tar.bz2
#git://anongit.freedesktop.org/nouveau/xf86-video-nouveau
Source0: %{tarball}.tar.gz
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
%setup -q -n xf86-video-nouveau
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
* Fri Oct 23 2015 cjacker - 1.0.11-5.git
- Rebuild for new 4.0 release

* Fri Sep 04 2015 Cjacker <cjacker@foxmail.com>
- add patch1, should fix build with xorg-server 1.8rc1, althouth we did not update yet.
* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to git master.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

