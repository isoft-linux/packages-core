%define debug_package %{nil}
#this is a very early git codes
#by cjacker.

%define tarball xf86-video-virgl
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary: Xorg virgl video driver
Name: xorg-x11-drv-virgl
Version: 0.0.01
Release: 2.git
URL: http://cgit.freedesktop.org/~airlied/xf86-video-virgl 
License: MIT

# git clone git://people.freedesktop.org/~airlied/xf86-video-virgl
Source0: %{tarball}.tar.gz

Patch0: virgl-fix-build-with-xorg-1.9.patch
 
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

BuildRequires: libXfont-devel

BuildRequires: xcb-util
Requires: xorg-x11-server-Xorg >= 1.1.0-1

%description 
X.Org X11 VirGL video driver.

%prep
%setup -q -n %{tarball} 
%patch0 -p1

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
#%{_mandir}/man4/amdgpu*
#%{_datadir}/X11/xorg.conf.d/10-amdgpu.conf

%changelog
* Tue Nov 29 2016 cjacker - 0.0.01-2.git
- Update

