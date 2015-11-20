#control wheather build debuginfo package or not.
%global with_debuginfo 1

%define debuginfodir /usr/lib/debug

%define kversion 4.4.0
%define release 5

%define extraversion -%{release}

%define KVERREL %{version}-%{release}

%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%ifarch x86_64
%define asmarch x86
%endif

# Architectures we build tools/cpupower on
%define cpupowerarchs %{ix86} x86_64

Name: kernel
Summary: The Linux kernel (the core of the Linux operating system)
License: GPLv2
Version: %{kversion}
Release: %{release}
ExclusiveArch: noarch x86_64
ExclusiveOS: Linux
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{kversion}-%{release}
Requires(pre): kmod, grub, dracut 
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

#
# List the packages used during the kernel build
#
BuildRequires: kmod, patch, bash, sh-utils, tar, git
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, make, diffutils, gawk
BuildRequires: gcc, binutils busybox
BuildRequires: net-tools, hostname, bc

BuildRequires: libelfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel
BuildRequires: numactl-devel

%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
%define debuginfo_args --strict-build-id -r
%endif

#for kernel tools
BuildRequires: pciutils-devel gettext ncurses-devel

Source0: linux-%{kversion}.tar.xz

#amdgpu with powerplay
#git clone --depth 1 -b "amdgpu-powerplay" git://people.freedesktop.org/~agd5f/linux amdgpu
#tar drivers/gpu/drm/amd.
Source1: amd.tar.gz 

Source20: kernel-%{kversion}-x86_64.config

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config

# build tweak for build ID magic, even for -vanilla
Source3000: kbuild-AFTER_LINK.patch
 
Patch0: linux-tune-cdrom-default.patch

#Start amdgpu
#Enabel amdgpu powerplay Kconfig
Patch1: linux-add-amdgpu-powerplay-config.patch
#amd added drm_pcie_get_max_link_width to drm.
Patch2: amdgpu-add-drm_pcie_get_max_link_width-helper.patch 
#End amdgpu

Patch450: input-kill-stupid-messages.patch
Patch452: no-pcspkr-modalias.patch

Patch470: die-floppy-die.patch

Patch601: amd-xgbe-a0-Add-support-for-XGBE-on-A0.patch
Patch602: amd-xgbe-phy-a0-Add-support-for-XGBE-PHY-on-A0.patch
Patch603: ath9k-rx-dma-stop-check.patch
Patch604: disable-i8042-check-on-apple-mac.patch
Patch606: drm-i915-turn-off-wc-mmaps.patch
Patch607: drm-i915-hush-check-crtc-state.patch

Patch608: Input-synaptics-pin-3-touches-when-the-firmware-repo.patch
Patch609: scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch
Patch611: watchdog-Disable-watchdog-on-virtual-machines.patch
Patch612: xen-pciback-Don-t-disable-PCI_COMMAND-on-PCI-device-.patch

Patch615: 0001-iwlwifi-Add-new-PCI-IDs-for-the-8260-series.patch
Patch616: RDS-fix-race-condition-when-sending-a-message-on-unb.patch
 
#http://patchwork.ozlabs.org/patch/522709/
Patch2000: netfilter-ftp-irc-sane-sip-tftp-Fix-the-kernel-panic-when-load-these-modules-with-duplicated-ports.patch

#nouveau add dummy func to gk20a
Patch2002: nouveau-gk20a-add-dummy-func-to-avoid-null.patch

#already upstream, should removed later
#http://patchwork.ozlabs.org/patch/544307/
Patch2003: net-fix-feature-changes-on-device-without-ndo-set-features.patch

#https://bugs.freedesktop.org/show_bug.cgi?id=92638
#It should be removed later.
Patch2004: drm-i915-Ensure-associated-VMAs-are-inactive-when-contexts-are-destroyed.patch

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root-%{_target_cpu}


%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

%package devel
Summary: Development package for building kernel modules to match the kernel.
AutoReqProv: no
Provides: kernel-devel-%{_target_cpu} = %{kversion}-%{release}
Requires(pre): /usr/bin/find

%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.


%package headers
Summary: Header files for the Linux kernel for use by glibc

%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package -n kernel-tools
Summary: Assortment of tools for the Linux kernel
License: GPLv2
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{version}-%{release}
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
License: GPLv2
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.


%package -n kernel-tools-debuginfo
Summary: Debug information for package kernel-tools
Requires: %{name}-debuginfo = %{version}-%{release}
AutoReqProv: no
%description -n kernel-tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|.*%%{_bindir}/tmon(\.debug)?|XXX' -o kernel-tools-debuginfo.list}


%package debuginfo
Summary: Kernel debuginfo package

%description debuginfo
This package kernel debug files.


%package -n perf
Summary: Performance monitoring for the Linux kernel
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
Summary: Debug information for package perf
Requires: %{name}-debuginfo = %{version}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/traceevent/plugins/.*|XXX' -o perf-debuginfo.list}

%package -n python-perf
Summary: Python bindings for apps which will manipulate perf events
%description -n python-perf
The python-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%package -n python-perf-debuginfo
Summary: Debug information for package perf python bindings
Requires: %{name}-debuginfo = %{version}-%{release}
AutoReqProv: no
%description -n python-perf-debuginfo
This package provides debug information for the perf python bindings.

# the python_sitearch macro should already be defined from above
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{python_sitearch}/perf.so(\.debug)?|XXX' -o python-perf-debuginfo.list}


%prep
if [ ! -d kernel-%{kversion}/vanilla ]; then
%setup -q -n %{name}-%{version} -c
  mv linux-%{kversion} vanilla
  #start amdgpu
  rm -rf vanilla/drivers/gpu/drm/amd
  tar zxf %{SOURCE1} -C vanilla/drivers/gpu/drm
  pushd vanilla
  cat %{PATCH1} |patch -p1
  cat %{PATCH2} |patch -p1
  popd
  #end amdgpu
else 
  cd kernel-%{kversion}
  if [ -d linux-%{kversion}.%{_target_cpu} ]; then
     rm -rf deleteme.%{_target_cpu}
     mv linux-%{kversion}.%{_target_cpu} deleteme.%{_target_cpu}
     rm -rf deleteme.%{_target_cpu} &
  fi
fi

cp -rl vanilla linux-%{kversion}.%{_target_cpu}

cd linux-%{kversion}.%{_target_cpu}

# The kbuild-AFTER_LINK patch is needed regardless
cat %{SOURCE3000} |patch -p1

%patch0 -p1

%patch450 -p1
%patch452 -p1
%patch470 -p1

%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch604 -p1
%patch606 -p1
%patch607 -p1
%patch608 -p1
%patch609 -p1
%patch611 -p1
%patch612 -p1

%patch615 -p1
%patch616 -p1

%patch2000 -p1
%patch2002 -p1

%patch2003 -p1

%patch2004 -p1

# END OF PATCH APPLICATIONS


# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

cd ..

#======================================================
#perf_make macro
#parallel build seems broken in kernel-4.4
%global perf_make \
  make -s EXTRA_CFLAGS="${RPM_OPT_FLAGS}" -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 prefix=%{_prefix}
  #make -s EXTRA_CFLAGS="${RPM_OPT_FLAGS}" %{?_smp_mflags} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 prefix=%{_prefix}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%define __debug_install_post \
  /usr/lib/rpm/find-debuginfo.sh %{debuginfo_args} %{_builddir}/%{?buildsubdir}\
%{nil}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo
%defattr(-,root,root)
%endif

%endif
#======================================================

%build

#work with SOURCE2000, it's patch but should always be applied.
%if %{with_debuginfo}
# This override tweaks the kernel makefiles so that we run debugedit on an
# object before embedding it.  When we later run find-debuginfo.sh, it will
# run debugedit again.  The edits it does change the build ID bits embedded
# in the stripped object, but repeating debugedit is a no-op.  We do it
# beforehand to get the proper final build ID bits into the embedded image.
# This affects the vDSO images in vmlinux, and the vmlinux image in bzImage.
export AFTER_LINK=\
'sh -xc "/usr/lib/rpm/debugedit -b $$RPM_BUILD_DIR -d /usr/src/debug \
                                -i $@ > $@.id"'
%endif


pushd linux-%{kversion}.%{_target_cpu}

#build kernel
echo BUILDING A KERNEL FOR %{_target_cpu}...

make -s mrproper

#copy config file.
cp %{SOURCE20} .config

sed -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = %{extraversion}/" Makefile

make -s ARCH=%_target_cpu oldnoconfig > /dev/null
make -s ARCH=%_target_cpu %{?_smp_mflags} bzImage 
make -s ARCH=%_target_cpu %{?_smp_mflags} modules || exit 1

# perf
%{perf_make} DESTDIR=$RPM_BUILD_ROOT all

#build kernel tools
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
%endif
pushd tools/thermal/tmon/
make
popd


popd #linux-%{kversion}.%{_target_cpu}



%install
rm -rf $RPM_BUILD_ROOT

# Start installing the results
pushd linux-%{kversion}.%{_target_cpu}

#kernel Image and related files.
mkdir -p $RPM_BUILD_ROOT/boot

%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
%endif

install -m 644 .config $RPM_BUILD_ROOT/boot/config-%{KVERREL}
install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-%{KVERREL}
touch $RPM_BUILD_ROOT/boot/initrd-%{KVERREL}.img
cp arch/%{asmarch}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{KVERREL}

if [ -f arch/%{asmarch}/boot/zImage.stub ]; then
  cp arch/%{asmarch}/boot/zImage.stub $RPM_BUILD_ROOT/boot/zImage.stub-%{KVERREL} || :
fi

#Modules
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}
make -s ARCH=%_target_cpu INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=%{KVERREL}


#Devel
rm -f $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build
rm -f $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/source
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build
(cd $RPM_BUILD_ROOT/lib/modules/%{KVERREL} ; ln -s build source)

#--------------------------------------------------------------------
%if %{with_debuginfo}
    if test -s vmlinux.id; then
      cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/vmlinux.id
    else
      echo >&2 "*** ERROR *** no vmlinux build ID! ***"
      exit 1
    fi
    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/%{KVERREL}
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/%{KVERREL}
%endif
#--------------------------------------------------------------------


# first copy everything
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build
cp Module.symvers $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build


# then drop all but the needed Makefiles/Kconfig files
rm -rf $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/Documentation
rm -rf $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/scripts
rm -rf $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include
cp .config $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build
cp -a scripts $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build
if [ -d arch/%{asmarch}/scripts ]; then
  cp -a arch/%{asmarch}/scripts $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/arch/%{asmarch} || :
fi
if [ -f arch/%{asmarch}/*lds ]; then
  cp -a arch/%{asmarch}/*lds $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/arch/%{asmarch}/ || :
fi
rm -f $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/scripts/*.o
rm -f $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/scripts/*/*.o
if [ -d arch/%{asmarch}/include ]; then
  cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/
fi

mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include
pushd include
cp -a uapi xen acpi config crypto keys linux math-emu media net pcmcia rdma rxrpc scsi sound trace video asm-generic $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include
asmdir="../arch/%{asmarch}/include/asm"
cp -a $asmdir $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/
ln -s asm-$Arch $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/asm
# generated/*.h is necessary
# generated/uapi/linux/version.h is necessary
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/generated/
install -m644 ./generated/*.h $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/generated/
install -m644 ./generated/uapi/linux/version.h $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/generated/
popd

pushd $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/linux/
ln -fs ../generated/*.h .
popd

# Make sure the Makefile and version.h have a matching timestamp so that
# external modules can be built
touch -r $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/linux/version.h
touch -r $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/.config $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/linux/autoconf.h

# Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
cp $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/.config $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/build/include/config/auto.conf


# Install kernel headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install
# remove drm headers, libdrm-2.4.1 is OK.
rm -rf $RPM_BUILD_ROOT/usr/include/drm

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# dirs for additional modules per module-init-tools, kbuild/modules.txt
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/extra
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/updates
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/weak-updates

#fix modules perms.
find $RPM_BUILD_ROOT/lib/modules/%{KVERREL} -name "*.ko" -type f >modnames

# mark modules executable so that strip-to-file can strip them
cat modnames | xargs chmod u+x



# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT lib=%{_lib} install-bin install-traceevent-plugins
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext


#install kernel tools
%ifarch %{cpupowerarchs}
make -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%endif
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd 
#end install kernel tools
popd


#if with_debuginfo, we should not strip modules.
# Strip modules...
#pushd $RPM_BUILD_ROOT/lib/modules
#find . -name "*.ko" |xargs strip -R .comment --strip-unneeded
#popd

# Remove all firmwares provided by kernel.
# They are all in linux-firmware and other firmware packages.
rm -rf %{buildroot}/lib/firmware/*

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

%post
depmod -a %{KVERREL} >/dev/null ||:
dracut -f /boot/initrd-%{KVERREL}.img %{KVERREL} >/dev/null ||:
#mkinitcpio -g /boot/initrd-%{kversion}-%{release}.img -k %{kversion}-%{release}||:
grub-mkconfig -o /boot/grub/grub.cfg >/dev/null ||:

%postun
grub-mkconfig -o /boot/grub/grub.cfg >/dev/null ||:

%preun

%post -n kernel-tools -p /sbin/ldconfig

%postun -n kernel-tools -p /sbin/ldconfig


%files
%defattr(-,root,root)
/boot/vmlinuz-%{KVERREL}
/boot/System.map-%{KVERREL}
/boot/config-%{KVERREL}
%dir /lib/modules/%{KVERREL}
/lib/modules/%{KVERREL}/modules.order
/lib/modules/%{KVERREL}/modules.builtin
/lib/modules/%{KVERREL}/kernel
/lib/modules/%{KVERREL}/extra
/lib/modules/%{KVERREL}/updates
/lib/modules/%{KVERREL}/weak-updates
%dir /lib/firmware

%exclude /lib/modules/%{KVERREL}/build
%exclude /lib/modules/%{KVERREL}/source

%ghost /boot/initrd-%{KVERREL}.img
%ghost /lib/modules/%{KVERREL}/modules.alias
%ghost /lib/modules/%{KVERREL}/modules.alias.bin
%ghost /lib/modules/%{KVERREL}/modules.builtin.bin
%ghost /lib/modules/%{KVERREL}/modules.dep
%ghost /lib/modules/%{KVERREL}/modules.dep.bin
%ghost /lib/modules/%{KVERREL}/modules.devname
%ghost /lib/modules/%{KVERREL}/modules.softdep
%ghost /lib/modules/%{KVERREL}/modules.symbols
%ghost /lib/modules/%{KVERREL}/modules.symbols.bin



%files devel
%defattr(-,root,root)
%verify(not mtime) /lib/modules/%{KVERREL}/build
%verify(not mtime) /lib/modules/%{KVERREL}/source


%files headers
%defattr(-,root,root)
/usr/include/*


%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%dir %{_libdir}/traceevent/plugins
%{_libdir}/traceevent/plugins/*
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_datadir}/perf-core/*
%{_sysconfdir}/bash_completion.d/perf

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo
%defattr(-,root,root)

%files -f python-perf-debuginfo.list -n python-perf-debuginfo
%defattr(-,root,root)
%endif

%files -n kernel-tools -f cpupower.lang
%defattr(-,root,root)
%ifarch %{cpupowerarchs}
%{_bindir}/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%{_bindir}/tmon
%endif

%if %{with_debuginfo}
%files -f kernel-tools-debuginfo.list -n kernel-tools-debuginfo
%defattr(-,root,root)
%endif

%ifarch %{cpupowerarchs}
%files -n kernel-tools-libs
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.0

%files -n kernel-tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif


%changelog
* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-5
- Enable more drivers

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-4
- P2004, Ensure associated VMAs are inactive when contexts are destroyed
- Should fix "i915_gem_context_free WARN_ON(!list_empty(&ppgtt->base.active_list))"

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-3
- Update amdgpu powerplay

* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-2
- Update to 4.4.0rc1
- drop virgl backport patch, already in mainline
- drop various platform backport patches, already in mainline.
- keep amdgpu powerplay backport.
- enable CONFIG_X86_VERBOSE_BOOTUP again, we alread have correct grub smooth transition.

* Sat Nov 14 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-128
- backport virious platform driver fixes.
- update to latest amdgpu drm codes.
- backport virgl support from linux-next.

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-122
- Backport amdgpu powerplay

* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-121
- Add check of nouveau device pmu, try fix dell vostro 2421 issue

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-120
- Update to kernel-4.3.0 official release

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-119
- Rebuild, rename debuginfo package name

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-118
- Enable kernel debuginfo package and perf tools

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.3.0-117
- Update to 4.3.0 rc7

* Fri Oct 23 2015 cjacker <cjacker@foxmail.com> - 4.3.0-113
- Rebuild for new 4.0 release

* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com>
- update to 4.3.0rc6.

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- fix crash when 'insmod nf_conntrack_ftp.ko ports=76,76'
- tune ipv6 releted options, build ipv6 into kernel

* Mon Oct 05 2015 Cjacker <cjacker@foxmail.com>
- update to 4.3.0-rc4

* Tue Sep 29 2015 Cjacker <cjacker@foxmail.com>
- update to 4.3.0-rc3

* Tue Aug 25 2015 Cjacker <cjacker@foxmail.com>
- tune kernel config file. hope to fix usb issue from Yetist.

* Mon Aug 24 2015 Cjacker <cjacker@foxmail.com>
- update to 4.2.0rc8
- remove dell sound noise fix, already upstream.

* Wed Aug 19 2015 Cjacker <cjacker@foxmail.com>
- build kernel-tools package.

* Mon Aug 17 2015 Cjacker <cjacker@foxmail.com>
- update to 4.2rc7
- enable intel prelimitary support in drm.
- remove Group from spec

* Sat Aug 15 2015 Cjacker <cjacker@foxmail.com>
- update to 4.2rc6
- disable AMDGPU_CIK currently, radeon driver provide better support.
 
* Mon Aug 03 2015 Cjacker <cjacker@foxmail.com>
- update to 4.2-rc5

* Sun Aug 02 2015 Cjacker <cjacker@foxmail.com>
- enable smack LSM
- add kdbus

* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- update to rc3
