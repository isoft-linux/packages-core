Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.64
Release: 4 
License: MIT
URL: http://dri.sourceforge.net
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2

#git://anongit.freedesktop.org/mesa/drm
#git repos, we just keep it here to "git pull"
Source1: drm.tar.gz

Source2: 91-drm-modeset.rules

# hardcode the 666 instead of 660 for device nodes
Patch3: libdrm-make-dri-perms-okay.patch
# remove backwards compat
Patch4: libdrm-2.4.0-no-bc.patch
# make rule to print the list of test programs
Patch5: libdrm-2.4.25-check-programs.patch

Requires: libpciaccess
BuildRequires: pkgconfig automake autoconf libtool

BuildRequires: kernel-headers libpthread-stubs-devel
BuildRequires: libpciaccess-devel


%description
Direct Rendering Manager runtime library

%package devel
Summary: Direct Rendering Manager development package
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers 

%description devel
Direct Rendering Manager development package

%package -n drm-utils
Summary: Direct Rendering Manager utilities

%description -n drm-utils
Utility programs for the kernel DRM interface.

%prep
%setup -q
%patch3 -p1 -b .forceperms
%patch4 -p1 -b .no-bc
%patch5 -p1 -b .check

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
#2.4.64 need autoreconf
autoreconf -ivf
%configure \
    --enable-install-test-programs \
    --enable-udev \
    --enable-libkms \
    --enable-intel \
    --enable-radeon \
    --enable-nouveau \
    --enable-vmwgfx \
    --enable-amdgpu \
    --enable-manpages 
make %{?_smp_mflags}

pushd tests
make %{?smp_mflags} `make check-programs`
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

pushd tests
mkdir -p %{buildroot}%{_bindir}
for foo in $(make check-programs) ; do
 install -m 0755 .libs/$foo %{buildroot}%{_bindir}
done
popd


# SUBDIRS=libdrm
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/


find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/91-drm-modeset.rules

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

%files -n drm-utils
%{_bindir}/dristat
%{_bindir}/drmstat
%{_bindir}/getclient
%{_bindir}/getstats
%{_bindir}/getversion
%{_bindir}/name_from_fd
%{_bindir}/openclose
%{_bindir}/setversion
%{_bindir}/updatedraw
%{_bindir}/modetest
%{_bindir}/modeprint
%{_bindir}/vbltest
%{_bindir}/kmstest
%exclude %{_bindir}/exynos*
%exclude %{_bindir}/drmsl
%exclude %{_bindir}/hash
%exclude %{_bindir}/proptest
%exclude %{_bindir}/random

%changelog
* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- finally, libdrm-2.4.63 have amdgpu support.

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to c8df9e7

* Thu Aug 06 2015 Cjacker <cjacker@foxmail.com>
- amdgpu in mainline, update.

* Sun Jul 26 2015 Cjacker <cjacker@foxmail.com>
- add amdgpu-in-development codes.
- should remove when it enter mainline.
