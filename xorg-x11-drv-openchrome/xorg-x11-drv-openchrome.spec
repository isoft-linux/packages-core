%define debug_package %{nil}
%define tarball xf86-video-openchrome
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary:        Xorg X11 openchrome video driver
Name:           xorg-x11-drv-openchrome
Version:        0.5.0
Release:        2
URL:            http://www.freedesktop.org/wiki/Openchrome/
License:        MIT

Source0:        http://xorg.freedesktop.org/archive/individual/driver/%{tarball}-%{version}.tar.bz2

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  automake autoconf libtool
BuildRequires:  xorg-x11-server-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libXvMC-devel

BuildRequires:  libdrm-devel >= 2.0-1
Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)

Obsoletes:      xorg-x11-drv-via <= 0.2.2-4
Provides:       xorg-x11-drv-via = 0.2.2-5

%description 
X.Org X11 openchrome video driver.

%package devel
Summary:        Xorg X11 openchrome video driver XvMC development package
Requires:       %{name} = %{version}-%{release}

%description devel
X.Org X11 openchrome video driver XvMC development package.

%prep
%setup -q -n %{tarball}-%{version}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure --disable-static --enable-viaregtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --


%clean
rm -rf $RPM_BUILD_ROOT


%post

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{driverdir}/openchrome_drv.so
%{_libdir}/libchromeXvMC.so.1
%{_libdir}/libchromeXvMC.so.1.0.0
%{_libdir}/libchromeXvMCPro.so.1
%{_libdir}/libchromeXvMCPro.so.1.0.0
%{_mandir}/man4/openchrome.4.gz
%{_sbindir}/via_regs_dump

%files devel
%defattr(-,root,root,-)
%{_libdir}/libchromeXvMC.so
%{_libdir}/libchromeXvMCPro.so

%changelog
* Tue Nov 29 2016 cjacker - 0.5.0-2
- Update

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 0.3.3-16.git
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 0.3.3-15.git
- Rebuild for new 4.0 release

