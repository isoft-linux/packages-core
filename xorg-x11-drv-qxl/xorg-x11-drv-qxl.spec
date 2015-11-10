%define debug_package %{nil}
%global tarball xf86-video-qxl
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers

# Xspice is x86_64 only since spice-server is x86_64 only
%ifarch x86_64
%define with_xspice 0 
%else
%define with_xspice 0
%endif

#% global gitdate 20130703
%global gitversion 8b03ec16

%if 0%{?gitdate}

%define gver .%{gitdate}git%{gitversion}
%endif

Summary:   Xorg X11 qxl video driver
Name:      xorg-x11-drv-qxl

Version:   0.1.4

Release:   7%{?gver}%{?dist}
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2

#Source0: %{tarball}-%{gitdate}.tar.bz2
Patch1:    qxl-kms-disable-composite.patch

Patch3: no-surfaces-kms.patch
Patch4: 0001-worst-hack-of-all-time-to-qxl-driver.patch
Patch5: qxl-aarch64.patch

# Upstream commits
Patch6: 0006-Use-for-system-includes.patch
Patch7: 0007-Fix-compilation-with-newer-Xorg-versions.patch


License:   MIT

ExcludeArch: s390 s390x

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-devel >= 1.1.0-1
BuildRequires: spice-protocol >= 0.12.1
BuildRequires: libdrm-devel >= 2.4.46-1

%if %{with_xspice}
BuildRequires: libspice-devel >= 0.8.0
%endif

BuildRequires: glib2-devel
BuildRequires: libtool
BuildRequires: libudev-devel
BuildRequires: libXfont-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description
X.Org X11 qxl video driver.

%if %{with_xspice}
%package -n    xorg-x11-server-Xspice
Summary:       XSpice is an X server that can be accessed by a Spice client
Requires:      Xorg %(xserver-sdk-abi-requires ansic)
Requires:      Xorg %(xserver-sdk-abi-requires videodrv)
Requires:      xorg-x11-server-Xorg
Requires:      python >= 2.6

%description -n xorg-x11-server-Xspice
XSpice is both an X and a Spice server.
%endif

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
#autoreconf -f -i
%if %{with_xspice}
%define enable_xspice --enable-xspice
%endif
%configure --disable-static %{?enable_xspice}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%ifarch x86_64
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11
install -p -m 644 examples/spiceqxl.xorg.conf.example \
    $RPM_BUILD_ROOT%{_sysconfdir}/X11/spiceqxl.xorg.conf
# FIXME: upstream installs this file by default, we install it elsewhere.
# upstream should just not install it and let dist package deal with
# doc/examples.
rm -f $RPM_BUILD_ROOT/usr/share/doc/xf86-video-qxl/spiceqxl.xorg.conf.example
%if !%{with_xspice}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/spiceqxl.xorg.conf
%endif
%endif


%files
%doc COPYING README
%{driverdir}/qxl_drv.so

%if %{with_xspice}
%files -n xorg-x11-server-Xspice
%doc COPYING README.xspice README examples/spiceqxl.xorg.conf.example
%config(noreplace) %{_sysconfdir}/X11/spiceqxl.xorg.conf
%{_bindir}/Xspice
%{driverdir}/spiceqxl_drv.so
%endif


%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 0.1.4-7
- Rebuild with xorg-server 1.8.0

* Fri Oct 23 2015 cjacker - 0.1.4-6
- Rebuild for new 4.0 release

