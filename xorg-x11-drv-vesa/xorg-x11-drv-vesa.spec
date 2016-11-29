%define debug_package %{nil}
%define tarball xf86-video-vesa
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers


Summary:   Xorg X11 vesa video driver
Name:      xorg-x11-drv-vesa
Version:   2.3.4
Release:   7 
URL:       http://www.x.org
Source0:   xf86-video-vesa-%{version}.tar.bz2 
License:   MIT/X11

ExclusiveArch: %{ix86} x86_64 ia64 ppc alpha sparc sparc64

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk

Requires:  xorg-x11-server-Xorg
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)


%description 
X.Org X11 vesa video driver.

%prep
%setup -q -n xf86-video-vesa-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/vesa_drv.so
%{_mandir}/man4/vesa.4*

%changelog
* Tue Nov 29 2016 cjacker - 2.3.4-7
- Update

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 2.3.4-6
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 2.3.4-5
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

