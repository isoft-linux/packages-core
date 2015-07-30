Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.62
Release: 3 
License: MIT
Group:  Core/Runtime/Library
URL: http://dri.sourceforge.net
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.gz
Patch0: 5ba34e1aeed3c343bc9b53727220449d244b3296.patch  
Patch1: 5c68f9f6f9bcc7edeacbc18b1052aed46a89c9f2.patch 
Patch2: intel_leak_the_userptr_test_bo.patch

Requires: libpciaccess
BuildRequires: pkgconfig automake autoconf libtool

BuildRequires: kernel-headers libpthread-stubs-devel
BuildRequires: libpciaccess-devel

Source2: 91-drm-modeset.rules
Source3: i915modeset

%description
Direct Rendering Manager runtime library

%package devel
Summary: Direct Rendering Manager development package
Group: Core/Development/Library
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers 

%description devel
Direct Rendering Manager development package

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%configure \
    --enable-udev \
    --enable-libkms \
    --enable-intel \
    --enable-radeon \
    --enable-nouveau \
    --enable-vmwgfx \
    --enable-manpages 
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# SUBDIRS=libdrm
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/i915modeset.conf

find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/91-drm-modeset.rules
%{_sysconfdir}/modprobe.d/i915modeset.conf

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/libdrm
%dir %{_includedir}/libkms
%{_includedir}/*.h
%{_includedir}/libdrm/*
%{_includedir}/libkms/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/drmAvailable.3.gz
%{_mandir}/man3/drmHandleEvent.3.gz
%{_mandir}/man3/drmModeGetResources.3.gz
%{_mandir}/man7/drm-gem.7.gz
%{_mandir}/man7/drm-kms.7.gz
%{_mandir}/man7/drm-memory.7.gz
%{_mandir}/man7/drm-mm.7.gz
%{_mandir}/man7/drm-ttm.7.gz
%{_mandir}/man7/drm.7.gz

%changelog
