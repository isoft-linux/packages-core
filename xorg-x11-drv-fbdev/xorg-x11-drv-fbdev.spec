%define debug_package %{nil}
%define tarball xf86-video-fbdev
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

Summary:   Xorg X11 fbdev video driver
Name:      xorg-x11-drv-fbdev
Version:   0.4.4
Release:   5 
URL:       http://www.x.org
Source0:   xf86-video-fbdev-%{version}.tar.bz2 
License:   MIT/X11
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch: %{ix86} x86_64 ia64 ppc alpha sparc sparc64

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk

Requires: xorg-x11-server-Xorg
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 fbdev video driver.

%prep
%setup -q -n xf86-video-fbdev-%{version}
%build
%configure
make %{?_smp_mflags}

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
%dir %{moduledir}
%dir %{driverdir}
%{driverdir}/fbdev_drv.so
#%dir %{_mandir}/man4x
%{_mandir}/man4/fbdev.4*

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 0.4.4-5
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 0.4.4-4
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

