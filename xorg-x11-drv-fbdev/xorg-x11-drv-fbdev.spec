%define tarball xf86-video-fbdev
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

Summary:   Xorg X11 fbdev video driver
Name:      xorg-x11-drv-fbdev
Version:   0.4.4
Release:   3 
URL:       http://www.x.org
Source0:   xf86-video-fbdev-%{version}.tar.bz2 
License:   MIT/X11
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch: %{ix86} x86_64 ia64 ppc alpha sparc sparc64

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk

Requires:  xorg-x11-server-Xorg

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

rpmclean
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
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

