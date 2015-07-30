%define tarball xf86-video-nouveau
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
Summary:   Xorg X11 nouveau video driver(s)
Name:      xorg-x11-drv-nouveau
Version:   1.0.11
Release:   2 
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Source0:   %{tarball}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.3.0
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: xcb-util
Requires:  xorg-x11-server-Xorg >= 1.1.0-1

%description 
X.Org X11 nouveau video driver.

%prep
%setup -q -n xf86-video-nouveau-%{version} 

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT || exit 1

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/*.so
%{_mandir}/man4/nouveau.4*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

