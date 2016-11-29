%define debug_package %{nil}
%global tarball xf86-input-vmmouse
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

#global gitdate 20101209
#global gitversion 07232feb6

Summary:    Xorg X11 vmmouse input driver
Name:	    xorg-x11-drv-vmmouse
Version:    13.1.0
Release:    4%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
URL:	    http://www.x.org
License:    MIT

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

# Yes, this is not the same as vmware.  Yes, this is intentional.
ExclusiveArch: %{ix86} x86_64

BuildRequires: xorg-x11-server-devel >= 1.10.99.902 systemd-devel
BuildRequires: automake autoconf libtool

Requires:  xorg-x11-server-Xorg
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)

%description 
X.Org X11 vmmouse input driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules \
    --with-xorg-conf-dir='%{_datadir}/X11/xorg.conf.d' \
    --with-udev-rules-dir=%{_prefix}/lib/udev/rules.d
make %{?_smp_mflags}

%install
%make_install

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# Don't need HAL no more
rm -rf $RPM_BUILD_ROOT/%{_libdir}/hal/hal-probe-vmmouse
rm -rf $RPM_BUILD_ROOT/%{_datadir}/hal/fdi/

%files
%{driverdir}/vmmouse_drv.so
%{_mandir}/man4/vmmouse.4*
%{_mandir}/man1/vmmouse_detect.1*
%{_bindir}/vmmouse_detect
%{_datadir}/X11/xorg.conf.d/50-vmmouse.conf
%{_prefix}/lib/udev/rules.d/*.rules

%changelog
* Tue Nov 29 2016 cjacker - 13.1.0-4
- Rebuild

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 13.1.0-3
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 13.1.0-2
- Rebuild for new 4.0 release

