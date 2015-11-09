%define dracutlibdir %{_prefix}/lib/dracut

Name: dracut
Version: 043
Release: 4 

Summary: Initramfs generator using udev
License: GPLv2+ and LGPLv2.1+
URL: https://dracut.wiki.kernel.org/
Source0: http://www.kernel.org/pub/linux/utils/boot/dracut/dracut-%{version}.tar.xz
Patch0: 0001-Fix-default-udev-systemd-dir-detection-in-usr-merge-.patch

BuildRequires: bash 

BuildRequires: pkgconfig

BuildRequires: systemd-units

Obsoletes: dracut-kernel < 005
Provides:  dracut-kernel = %{version}-%{release}

Requires: bash >= 4
Requires: coreutils
Requires: cpio
Requires: filesystem >= 2.1.0
Requires: findutils
Requires: grep
Requires: hardlink
Requires: gzip xz
Requires: kmod
Requires: sed
Requires: tar
Requires: util-linux >= 2.21
Requires: systemd >= 199
Requires: curl
Requires: mdadm
Requires: kbd
Requires: gnupg
Requires: btrfs-progs

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export CC=gcc

CFLAGS="-D_GNU_SOURCE" %configure \
    --systemdsystemunitdir=%{_unitdir} \
    --libdir=%{_prefix}/lib

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make %{?_smp_mflags} install \
     DESTDIR=$RPM_BUILD_ROOT \
     libdir=%{_prefix}/lib

echo "DRACUT_VERSION=%{version}-%{release}" > $RPM_BUILD_ROOT/%{dracutlibdir}/dracut-version.sh

rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/01fips
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/02fips-aesni

%if %{defined _unitdir}
# for systemd, better use systemd-bootchart
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00bootchart
%endif

# we do not support dash in the initramfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/00dash

# remove gentoo specific modules
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/50gensplash


# we do not support network in dracut
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/40network
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95fcoe
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95iscsi
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/90livenet
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/90qemu-net
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95cifs
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95nbd
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95nfs
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95ssh-client
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/45ifcfg
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95znet
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95dasd_rules
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95fcoe-uefi
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/95zfcp_rules


#remove some modules 
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/03modsign
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/05busybox
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/90crypt
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/97biosdevname


%if %{defined _unitdir}
# with systemd IMA and selinux modules do not make sense
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/96securityfs
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/97masterkey
rm -fr $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/98integrity
%endif

mkdir -p $RPM_BUILD_ROOT/boot/dracut
mkdir -p $RPM_BUILD_ROOT/var/lib/dracut/overlay
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
touch $RPM_BUILD_ROOT%{_localstatedir}/log/dracut.log
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/initramfs

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 dracut.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/dracut_log

# create compat symlink
mkdir -p $RPM_BUILD_ROOT/sbin
ln -s /usr/bin/dracut $RPM_BUILD_ROOT/sbin/dracut

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{_bindir}/dracut
# compat symlink
/sbin/dracut
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%{dracutlibdir}/dracut-functions.sh
%{dracutlibdir}/dracut-functions
%{dracutlibdir}/dracut-version.sh
%{dracutlibdir}/dracut-logger.sh
%{dracutlibdir}/dracut-initramfs-restore
%{dracutlibdir}/dracut-install
%config(noreplace) %{_sysconfdir}/dracut.conf
#%{dracutlibdir}/dracut.conf.d/01-dist.conf
%dir %{_sysconfdir}/dracut.conf.d
%dir %{dracutlibdir}/dracut.conf.d
%{_mandir}/man8/dracut.8*
%{_mandir}/man8/*service.8*
%{_mandir}/man8/mkinitrd.8*
%{_mandir}/man1/lsinitrd.1*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man7/dracut.bootup.7*
%{_mandir}/man5/dracut.conf.5*
%if %{defined _unitdir}
%{dracutlibdir}/modules.d/00systemd-bootchart
%else
%{dracutlibdir}/modules.d/00bootchart
%endif

/usr/lib/dracut/skipcpio
/usr/lib/kernel/install.d/50-dracut.install
/usr/lib/kernel/install.d/51-dracut-rescue.install
/usr/share/man/man7/dracut.modules.7.gz
/usr/share/man/man8/mkinitrd-suse.8.gz

#/usr/lib/kernel/install.d/50-dracut.install
#/usr/lib/kernel/install.d/51-dracut-rescue.install
%{dracutlibdir}/modules.d/00bash
%{dracutlibdir}/modules.d/00systemd
%{dracutlibdir}/modules.d/01systemd-initrd
%{dracutlibdir}/modules.d/02systemd-networkd
%{dracutlibdir}/modules.d/03rescue
#%{dracutlibdir}/modules.d/03modsign
%{dracutlibdir}/modules.d/04watchdog
#%{dracutlibdir}/modules.d/05busybox
%{dracutlibdir}/modules.d/10i18n
%{dracutlibdir}/modules.d/02caps
%{dracutlibdir}/modules.d/30convertfs
%{dracutlibdir}/modules.d/45url-lib
%{dracutlibdir}/modules.d/50drm
%{dracutlibdir}/modules.d/50plymouth
%{dracutlibdir}/modules.d/80cms
%{dracutlibdir}/modules.d/90btrfs
#%{dracutlibdir}/modules.d/90crypt
%{dracutlibdir}/modules.d/90dm
%{dracutlibdir}/modules.d/90dmraid
%{dracutlibdir}/modules.d/90dmsquash-live
%{dracutlibdir}/modules.d/90kernel-modules
%{dracutlibdir}/modules.d/90lvm
%{dracutlibdir}/modules.d/90mdraid
%{dracutlibdir}/modules.d/90multipath
%{dracutlibdir}/modules.d/90qemu
%{dracutlibdir}/modules.d/90kernel-network-modules
%{dracutlibdir}/modules.d/91crypt-gpg
%{dracutlibdir}/modules.d/91crypt-loop
%{dracutlibdir}/modules.d/95debug
%{dracutlibdir}/modules.d/95resume
%{dracutlibdir}/modules.d/95rootfs-block
%{dracutlibdir}/modules.d/95dasd
%{dracutlibdir}/modules.d/95dasd_mod
%{dracutlibdir}/modules.d/95fstab-sys
%{dracutlibdir}/modules.d/95zfcp
%{dracutlibdir}/modules.d/95terminfo
%{dracutlibdir}/modules.d/95udev-rules
%{dracutlibdir}/modules.d/95virtfs
%if %{undefined _unitdir}
%{dracutlibdir}/modules.d/96securityfs
%{dracutlibdir}/modules.d/97masterkey
%{dracutlibdir}/modules.d/98integrity
%endif
#%{dracutlibdir}/modules.d/97biosdevname
%{dracutlibdir}/modules.d/98ecryptfs
%{dracutlibdir}/modules.d/98pollcdrom
%{dracutlibdir}/modules.d/98selinux
%{dracutlibdir}/modules.d/98syslog
%{dracutlibdir}/modules.d/98dracut-systemd
%{dracutlibdir}/modules.d/98usrmount
%{dracutlibdir}/modules.d/99base
%{dracutlibdir}/modules.d/99fs-lib
%{dracutlibdir}/modules.d/99uefi-lib
%{dracutlibdir}/modules.d/99img-lib
%{dracutlibdir}/modules.d/99shutdown
%config(noreplace) %{_sysconfdir}/logrotate.d/dracut_log
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%dir %{_sharedstatedir}/initramfs

%if %{defined _unitdir}
%{_unitdir}/dracut-shutdown.service
%{_unitdir}/dracut-cmdline.service
%{_unitdir}/dracut-initqueue.service
%{_unitdir}/dracut-mount.service
%{_unitdir}/dracut-pre-mount.service
%{_unitdir}/dracut-pre-pivot.service
%{_unitdir}/dracut-pre-trigger.service
%{_unitdir}/dracut-pre-udev.service
%{_unitdir}/initrd.target.wants/dracut-cmdline.service
%{_unitdir}/initrd.target.wants/dracut-initqueue.service
%{_unitdir}/initrd.target.wants/dracut-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-mount.service
%{_unitdir}/initrd.target.wants/dracut-pre-pivot.service
%{_unitdir}/initrd.target.wants/dracut-pre-trigger.service
%{_unitdir}/initrd.target.wants/dracut-pre-udev.service
%{_unitdir}/sysinit.target.wants/dracut-shutdown.service


%endif

%{_datadir}/pkgconfig/dracut.pc
%{_mandir}/man8/dracut-catimages.8*
%{_bindir}/dracut-catimages
%dir /boot/dracut
%dir /var/lib/dracut
%dir /var/lib/dracut/overlay


%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 043-4
- Add patch0

* Fri Oct 23 2015 cjacker - 043-3
- Rebuild for new 4.0 release

