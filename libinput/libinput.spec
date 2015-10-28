Summary: libinput is a library to handle input devices in Wayland compositors and to provide a generic X.Org input driver. 
Name:    libinput 
Version: 1.1.0
Release: 4
License: GPL
Source0: http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz

BuildRequires: libevdev-devel
BuildRequires: mtdev-devel

%description
libinput is a library to handle input devices in Wayland compositors and to provide a generic X.Org input driver. It provides device detection, device handling, input device event processing and abstraction so minimize the amount of custom input code compositors need to provide the common set of functionality that users expect.

%package devel
Summary: Libraries and headers for %{name} 
Requires: %name = %{version}

%description devel
Libraries and headers for %{name}

%prep
%setup -q

%build
%configure \
    --disable-static

make %{?_smp_flags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/libinput-debug-events
%{_bindir}/libinput-list-devices
%{_libdir}/udev/hwdb.d/90-libinput-model-quirks.hwdb
%{_libdir}/udev/libinput-device-group
%{_libdir}/udev/rules.d/80-libinput-device-groups.rules
%{_libdir}/udev/rules.d/90-libinput-model-quirks.rules
#%{_libdir}/udev/80-libinput-device-groups-litest.rules
#%{_libdir}/udev/90-libinput-model-quirks-litest.rules
%{_libdir}/udev/libinput-model-quirks

%{_mandir}/man1/libinput-debug-events.1.gz
%{_mandir}/man1/libinput-list-devices.1.gz


%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-4
- Update to 1.1.0, support pointer acceleration profiles.

* Fri Oct 23 2015 cjacker - 1.0.2-3
- Rebuild for new 4.0 release

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-2
- Update to 1.0.2

* Thu Sep 03 2015 Cjacker <cjacker@foxmail.com>
- update to 1.0.1

* Fri Aug 21 2015 Cjacker <cjacker@foxmail.com>
- update to 0.99.1
* Tue Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update to 0.21.0
* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to 0.20.0
