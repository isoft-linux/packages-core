Summary: libinput is a library to handle input devices in Wayland compositors and to provide a generic X.Org input driver. 
Name:    libinput 
Version: 0.20.0 
Release: 1
License: GPL
Group:  Core/Runtime/Library
Source0: http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz

BuildRequires: libevdev-devel
BuildRequires: mtdev-devel

%description
libinput is a library to handle input devices in Wayland compositors and to provide a generic X.Org input driver. It provides device detection, device handling, input device event processing and abstraction so minimize the amount of custom input code compositors need to provide the common set of functionality that users expect.

%package devel
Summary: Libraries and headers for %{name} 
Group:   Core/Development/Library
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
rpmclean

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
%{_libdir}/udev/80-libinput-device-groups-litest.rules
%{_libdir}/udev/90-libinput-model-quirks-litest.rules
%{_libdir}/udev/libinput-model-quirks

%{_mandir}/man1/libinput-debug-events.1.gz
%{_mandir}/man1/libinput-list-devices.1.gz


%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to 0.20.0
