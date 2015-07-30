%define tarball xf86-video-vmware
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
%define gitdate 20150211
%define gitversion 8f0cf7c

%undefine _hardened_build

%if 0%{?gitdate}
%define gver .%{gitdate}git%{gitversion}
%endif

Summary:    Xorg X11 vmware video driver
Name:	    xorg-x11-drv-vmware
Version:    13.0.2
Release:    9%{?gver}%{?dist}
URL:	    http://www.x.org
License:    MIT
Group:	    User Interface/X Hardware Support

%if 0%{?gitdate}
Source0: %{tarball}-%{gitdate}.tar.bz2
%else
Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

ExclusiveArch: %{ix86} x86_64 ia64

%if 0%{?gitdate}
BuildRequires: autoconf automake libtool
%endif
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libdrm-devel pkgconfig(xext) pkgconfig(x11)
BuildRequires: mesa-libxatracker-devel >= 8.0.1-4

Requires:  xorg-x11-server-Xorg
Requires: mesa-libxatracker >= 8.0.1-4

%description 
X.Org X11 vmware video driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
%if 0%{?gitdate}
autoreconf -v --install || exit 1
%endif
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%{driverdir}/vmware_drv.so
%{_mandir}/man4/vmware.4*

%changelog
