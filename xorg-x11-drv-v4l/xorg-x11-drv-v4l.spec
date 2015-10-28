%define debug_package %{nil}
%define tarball xf86-video-v4l
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%undefine _hardened_build

Summary:   Xorg X11 v4l video driver
Name:      xorg-x11-drv-v4l
Version:   0.2.0
Release:   45%{?dist}
URL:       http://www.x.org
License:   MIT

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Patch0:    xorg-x11-drv-v4l-support_v4l2_only_drivers.patch
Patch1:    xf86-video-v4l-0.2.0-build-fix.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool

Requires:  xorg-x11-server-Xorg
Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 v4l video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1
%patch1 -p1

%build
autoreconf -vif
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/v4l_drv.so
%{_mandir}/man4/v4l.4*

%changelog
* Fri Oct 23 2015 cjacker - 0.2.0-45
- Rebuild for new 4.0 release

