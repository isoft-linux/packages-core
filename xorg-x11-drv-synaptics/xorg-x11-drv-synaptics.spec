%define debug_package %{nil}
%global tarball xf86-input-synaptics
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

Name:           xorg-x11-drv-synaptics
Summary:        Xorg X11 Synaptics touchpad input driver
Version:        1.9.0
Release:        2
URL:            http://www.x.org
License:        MIT

Source0:        ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source3:        50-synaptics.conf
Source4:        70-touchpad-quirks.rules


ExcludeArch:    s390 s390x

BuildRequires:  git
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  xorg-x11-server-devel >= 1.10.99.902
BuildRequires:  libX11-devel libXi-devel libXtst-devel
BuildRequires:  xorg-x11-util-macros >= 1.8.0
BuildRequires:  libevdev-devel
BuildRequires:  systemd-devel

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires xinput)
Requires:       libevdev
Requires:       libXi libXtst

Provides:       synaptics = %{version}-%{release}
Obsoletes:      synaptics < 0.15.0


%description
This is the Synaptics touchpad driver for the X.Org X server. The following
touchpad models are supported:
* Synaptics
* appletouch (Post February 2005 and October 2005 Apple Aluminium Powerbooks)
* Elantech (EeePC)
* bcm5974 (Macbook Air (Jan 2008), Macbook Pro Penryn (Feb 2008), iPhone
  (2007), iPod Touch (2008)

%package devel
Summary:        Xorg X11 synaptics input driver
Requires:       pkgconfig

%description devel
Development files for the Synaptics TouchPad for X.Org.

%prep
%setup -q -n %{tarball}-%{version}

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

install -d $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/50-synaptics.conf

install -d $RPM_BUILD_ROOT%{_udevrulesdir}
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_udevrulesdir}/70-touchpad-quirks.rules

%post
udevadm control --reload-rules || :

%postun
udevadm control --reload-rules || :

%files
%{_datadir}/X11/xorg.conf.d/50-synaptics.conf
%{driverdir}/synaptics_drv.so
%{_bindir}/synclient
%{_bindir}/syndaemon
%{_mandir}/man4/synaptics.4*
%{_mandir}/man1/synclient.1*
%{_mandir}/man1/syndaemon.1*
%{_udevrulesdir}/70-touchpad-quirks.rules

%files devel
%{_libdir}/pkgconfig/xorg-synaptics.pc
%{_includedir}/xorg/synaptics-properties.h

%changelog
* Tue Nov 29 2016 cjacker - 1.9.0-2
- Update

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.8.3-4
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 1.8.2-3
- Rebuild for new 4.0 release

