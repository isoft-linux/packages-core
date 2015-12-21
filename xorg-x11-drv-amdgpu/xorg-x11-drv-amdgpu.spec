%define debug_package %{nil}
#this is a very early git codes
#we know we will ship amdgpu support finally
#so Just added it.
#by cjacker.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#make sure, libdrm had amdgpu support. I already added the git codes.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

%define tarball xf86-video-amdgpu
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary: Xorg amdgpu video driver
Name: xorg-x11-drv-amdgpu
Version: 1.0.0 
Release: 12.git
URL: http://cgit.freedesktop.org/xorg/driver/xf86-video-amdgpu/
License: MIT

# git clone git://anongit.freedesktop.org/xorg/driver/xf86-video-amdgpu
Source0: %{tarball}-ea558e6.tar.gz

BuildRequires: pkgconfig
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.3.0
BuildRequires: xorg-x11-proto-devel
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: mesa-libgbm-devel
BuildRequires: libdrm-devel >= 2.4.62-3
#for libudev-devel
BuildRequires: systemd-devel

BuildRequires: xcb-util
Requires: xorg-x11-server-Xorg >= 1.1.0-1

%description 
X.Org X11 AMD video driver.

%prep
%setup -q -n xf86-video-amdgpu

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
    --enable-udev \
    --enable-glamor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/*.so
%{_mandir}/man4/amdgpu*
%{_datadir}/X11/xorg.conf.d/10-amdgpu.conf

%changelog
* Mon Dec 21 2015 Cjacker <cjacker@foxmail.com> - 1.0.0-12.git
- Regular update

* Sun Nov 22 2015 Cjacker <cjacker@foxmail.com> - 0.0.01-11.git
- Update

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 0.0.01-10.git
- Rebuild with xorg-server 1.8.0

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.0.01-9.git
- Update

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 0.0.01-8.git
- Update to git 3b0a3c8

* Fri Oct 23 2015 cjacker - 0.0.01-7.git
- Rebuild for new 4.0 release

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 55a4461

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to c9611a2
* Sun Jul 26 2015 Cjacker <cjacker@foxmail.com>
- add git codes.
