%define debug_package %{nil}
%define tarball xf86-input-libinput
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir   %{moduledir}/drivers

Summary:    Xorg X11 libinput input driver
Name:       xorg-x11-drv-libinput
Version:    0.15.0
Release:    3
URL:        http://ww.x.org
License:    MIT
Source0:    %{tarball}-%{version}.tar.bz2
Source1:    90-libinput.conf


BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.14.0
BuildRequires: libudev-devel libevdev-devel libinput-devel >= 0.6.0-3
BuildRequires: xorg-x11-util-macros

Requires: xkeyboard-config
Requires: libinput >= 0.8.0
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)

%description
A generic input driver for the X.Org X11 X server based on libinput,
supporting all devices.


%package devel
Summary:  Xorg X11 libinput input driver development package.
Requires: pkgconfig

%description devel
Xorg X11 libinput input driver development files.


%prep
%setup -q -n xf86-input-libinput-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

install -d $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/90-libinput.conf

%files
%{moduledir}/input/libinput_drv.so
%{_datadir}/X11/xorg.conf.d/90-libinput.conf
%{_mandir}/man4/libinput.4*

%files devel
%{_libdir}/pkgconfig/xorg-libinput.pc
%{_includedir}/xorg/libinput-properties.h

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 0.15.0-3
- Update, rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 0.14.0-2
- Rebuild for new 4.0 release

* Fri Sep 04 2015 Cjacker <cjacker@foxmail.com>
- update to 0.14.0
* Fri Aug 21 2015 Cjacker <cjacker@foxmail.com>
- update to 0.13.0
