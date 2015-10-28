Name: kmod
Version: 21	
Release: 3 
Summary: Linux kernel module management utilities

License: GPLv2+
URL: http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0: ftp://ftp.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz

Source1: weak-modules
#example blacklist.conf and blacklist pcspkr
Source2: blacklist.conf

Exclusiveos: Linux

BuildRequires: zlib-devel
BuildRequires: xz-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

Provides: module-init-tools = 4.0-1
Obsoletes: module-init-tools < 4.0-1
Provides: /sbin/modprobe

%description
The kmod package provides various programs needed for automatic
loading and unloading of modules under 2.6, 3.x, and later kernels, as well
as other module management programs. Device drivers and filesystems are two
examples of loaded and unloaded modules.

%package libs
Summary: Libraries to handle kernel module loading and unloading
License: LGPLv2+

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary: Header files for kmod development
Requires: %{name} = %{version}-%{release}

%description devel
The kmod-devel package provides header files used for development of
applications that wish to load or unload Linux kernel modules.

%prep
%setup -q

%build
export V=1
%configure \
  --with-zlib \
  --with-xz
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modprobe
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modinfo
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/insmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/rmmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/depmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/lsmod

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/ 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d

mkdir -p $RPM_BUILD_ROOT/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules

%check
#in chroot env, may fail
make check ||:

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/depmod.d
%dir %{_sysconfdir}/modprobe.d
%{_sysconfdir}/modprobe.d/blacklist.conf
%dir %{_prefix}/lib/modprobe.d
%{_bindir}/kmod
%{_sbindir}/modprobe
%{_sbindir}/modinfo
%{_sbindir}/insmod
%{_sbindir}/rmmod
%{_sbindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/weak-modules
%{_datadir}/bash-completion/completions/kmod
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*

%files libs
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%changelog
* Fri Oct 23 2015 cjacker - 21-3
- Rebuild for new 4.0 release

* Sat Sep 12 2015 Cjacker <cjacker@foxmail.com>
- clean spec file.

