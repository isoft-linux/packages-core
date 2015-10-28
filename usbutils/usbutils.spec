Name: usbutils
Version: 008
Release: 2 
Source:	https://www.kernel.org/pub/linux/utils/usb/usbutils/usbutils-%{version}.tar.xz
URL: https://www.kernel.org/pub/linux/utils/usb/usbutils/
License: GPLv2+
BuildRequires: autoconf, libtool, libusbx-devel
Summary: Linux USB utilities
Patch0: usbutils-008-hwdata-path.patch

%description 
This package contains utilities for inspecting devices connected to a
USB bus.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -ivf
%configure --sbindir=%{_sbindir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# usb.ids is shipped in hwdata; nuke and adjust .pc file
#sed -i 's|usbids=/usr/share/usb.ids|usbids=/usr/share/hwdata/usb.ids|' $RPM_BUILD_ROOT%{_datadir}/pkgconfig/usbutils.pc
%files
%defattr(-,root,root,-)
%{_mandir}/*/*
#%{_sbindir}/*
%{_bindir}/*
%{_datadir}/pkgconfig/usbutils.pc
#%{_datadir}/usb.ids*
%doc AUTHORS COPYING ChangeLog NEWS README

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 23 2015 cjacker - 008-2
- Rebuild for new 4.0 release

