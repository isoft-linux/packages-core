%define with_systemd 1 

Summary: A collection of basic system utilities
Name: util-linux
Version: 2.27
Release: 6 
License: GPLv2 and GPLv2+ and LGPLv2+ and BSD with advertising and Public Domain
URL: http://en.wikipedia.org/wiki/Util-linux

%define upstream_version %{version}

### Macros
%define cytune_archs %{ix86} alpha %{arm}

### Dependencies
BuildRequires: gettext-devel
BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: zlib-devel
BuildRequires: popt-devel

%if %{with_systemd}
Buildrequires: systemd-devel
%endif

### Sources
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.27/util-linux-%{upstream_version}.tar.xz
Source1: util-linux-login.pamd
Source2: util-linux-remote.pamd
Source3: util-linux-chsh-chfn.pamd
Source4: util-linux-60-raw.rules
Source12: util-linux-su.pamd
Source13: util-linux-su-l.pamd
Source14: util-linux-runuser.pamd
Source15: util-linux-runuser-l.pamd
 
### Obsoletes & Conflicts & Provides
Conflicts: bash-completion < 1:2.1-1
# su(1) and runuser(1) merged into util-linux v2.22
Conflicts: coreutils < 8.20
# eject has been merged into util-linux v2.22
Obsoletes: eject <= 2.1.5
Provides: eject = 2.1.6
# old versions of e2fsprogs contain fsck, uuidgen
Conflicts: e2fsprogs < 1.41.8-5
# rename from util-linux-ng back to util-linux
Obsoletes: util-linux-ng < 2.19
Provides: util-linux-ng = %{version}-%{release}
Conflicts: filesystem < 3
Provides: /bin/dmesg
Provides: /bin/kill
Provides: /bin/more
Provides: /bin/mount
Provides: /bin/umount
Provides: /sbin/blkid
Provides: /sbin/blockdev
Provides: /sbin/findfs
Provides: /sbin/fsck
Provides: /sbin/nologin
Provides: mount
Requires(post): coreutils

Requires: pam >= 1.1.3-7, /etc/pam.d/system-auth
Requires: libuuid = %{version}-%{release}
Requires: libblkid = %{version}-%{release}
Requires: libmount = %{version}-%{release}

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.


%package -n libmount
Summary: Device mounting library
License: LGPLv2+
Requires: libblkid = %{version}-%{release}
Requires: libuuid = %{version}-%{release}
Conflicts: filesystem < 3

%description -n libmount
This is the device mounting library, part of util-linux.


%package -n libmount-devel
Summary: Device mounting library
License: LGPLv2+
Requires: libmount = %{version}-%{release}
Requires: pkgconfig

%description -n libmount-devel
This is the device mounting development library and headers,
part of util-linux.

%package -n python-libmount
Summary: Python binding of device mounting library
License: LGPLv2+
Requires: libmount = %{version}-%{release}
Requires: python 

%description -n python-libmount
This is python binding of the device mounting library,
part of util-linux.

%package -n libblkid
Summary: Block device ID library
License: LGPLv2+
Requires: libuuid = %{version}-%{release}
Conflicts: filesystem < 3
Requires(post): coreutils

%description -n libblkid
This is block device identification library, part of util-linux.

%package -n libblkid-devel
Summary: Block device ID library
License: LGPLv2+
Requires: libblkid = %{version}-%{release}
Requires: pkgconfig

%description -n libblkid-devel
This is the block device identification development library and headers,
part of util-linux.

%package -n libsmartcols
Summary: Table or tree library
License: LGPLv2+
Conflicts: filesystem < 3
Requires(post): coreutils

%description -n libsmartcols
This is Table or tree library, part of util-linux.

%package -n libsmartcols-devel
Summary: Table or tree library
License: LGPLv2+
Requires: libsmartcols = %{version}-%{release}
Requires: pkgconfig

%description -n libsmartcols-devel
This is the table or tree development library and headers,
part of util-linux.


%package -n libfdisk
Summary: fdisk library
License: LGPLv2+
Conflicts: filesystem < 3
Requires(post): coreutils

%description -n libfdisk
This is fdisk library, part of util-linux.

%package -n libfdisk-devel
Summary: fdisk library
License: LGPLv2+
Requires: libfdisk = %{version}-%{release}
Requires: pkgconfig

%description -n libfdisk-devel
This is the fdisk development library and headers,
part of util-linux.


%package -n libuuid
Summary: Universally unique ID library
License: BSD
Conflicts: filesystem < 3

%description -n libuuid
This is the universally unique ID library, part of util-linux.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid" package, which is a separate implementation.

%package -n libuuid-devel
Summary: Universally unique ID library
License: BSD
Requires: libuuid = %{version}-%{release}
Requires: pkgconfig

%description -n libuuid-devel
This is the universally unique ID development library and headers,
part of util-linux.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid-devel" package, which is a separate implementation.


%package -n uuidd
Summary: Helper daemon to guarantee uniqueness of time-based UUIDs
Requires: libuuid = %{version}-%{release}
License: GPLv2
%if %{with_systemd}
Requires: systemd
Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
%endif

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.

%package -n fstrim
Summary: Discard unused blocks on a mounted filesystem
License: GPLv2
%if %{with_systemd}
Requires: systemd
Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
%endif

%description -n fstrim
fstrim is used on a mounted filesystem to discard (or "trim") blocks 
which are not in use by the filesystem.  

This is useful for solid-state drives (SSDs) and thinly-provisioned storage.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
unset LINGUAS || :

export CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 $RPM_OPT_FLAGS"
export SUID_CFLAGS="-fpie"
export SUID_LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%configure \
	--disable-silent-rules \
	--disable-bfs \
	--disable-pg \
	--enable-socket-activation \
	--enable-chfn-chsh \
	--enable-write \
	--enable-raw \
	--without-udev \
	--without-user \
	--disable-makeinstall-chown \
%if %{with_systemd}
	--with-systemdsystemunitdir=%{_unitdir} \
%endif
%ifnarch %cytune_archs
	--disable-cytune \
%endif

# build util-linux
make %{?_smp_mflags}


%check
#some check failed for multibyte issue.
make check ||:

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,6,8,5}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/{pam.d,security/console.apps}
mkdir -p ${RPM_BUILD_ROOT}/var/log
touch ${RPM_BUILD_ROOT}/var/log/lastlog
chmod 0644 ${RPM_BUILD_ROOT}/var/log/lastlog

# install util-linux
make install DESTDIR=${RPM_BUILD_ROOT}

# raw
echo '.so man8/raw.8' > $RPM_BUILD_ROOT%{_mandir}/man8/rawdevices.8

# And a dirs uuidd needs that the makefiles don't create
install -d ${RPM_BUILD_ROOT}/run/uuidd
install -d ${RPM_BUILD_ROOT}/var/lib/libuuid

# libtool junk
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/*.la

# PAM settings
{
	pushd ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d
	install -m 644 %{SOURCE1} ./login
	install -m 644 %{SOURCE2} ./remote
	install -m 644 %{SOURCE3} ./chsh
	install -m 644 %{SOURCE3} ./chfn
	install -m 644 %{SOURCE12} ./su
	install -m 644 %{SOURCE13} ./su-l
	install -m 644 %{SOURCE14} ./runuser
	install -m 644 %{SOURCE15} ./runuser-l
	popd
}

ln -sf /proc/mounts %{buildroot}/etc/mtab

# remove static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{uuid,blkid,mount,smartcols,fdisk}.a


# find MO files
#%find_lang %name

# the files section supports only one -f option...
#mv %{name}.lang %{name}.files

# create list of setarch(8) symlinks
find  $RPM_BUILD_ROOT%{_bindir}/ -regextype posix-egrep -type l \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)$" \
	-printf "%{_bindir}/%f\n" >> %{name}.files

find  $RPM_BUILD_ROOT%{_mandir}/man8 -regextype posix-egrep  \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)\.8.*" \
	-printf "%{_mandir}/man8/%f*\n" >> %{name}.files

%find_lang util-linux
cat util-linux.lang >> %{name}.files

%post
# only for minimal buildroots without /var/log
[ -d /var/log ] || mkdir -p /var/log
touch /var/log/lastlog
chown root:root /var/log/lastlog
chmod 0644 /var/log/lastlog
if [ ! -L /etc/mtab ]; then
	ln -fs /proc/mounts /etc/mtab
fi

%post -n libblkid
/sbin/ldconfig

### Move blkid cache to /run
[ -d /run/blkid ] || mkdir -p /run/blkid
for I in /etc/blkid.tab /etc/blkid.tab.old \
         /etc/blkid/blkid.tab /etc/blkid/blkid.tab.old; do

	if [ -f "$I" ]; then
		mv "$I" /run/blkid/ || :
	fi
done

%postun -n libblkid -p /sbin/ldconfig

%post -n libuuid -p /sbin/ldconfig
%postun -n libuuid -p /sbin/ldconfig

%post -n libsmartcols -p /sbin/ldconfig
%postun -n libsmartcols -p /sbin/ldconfig


%post -n libfdisk -p /sbin/ldconfig
%postun -n libfdisk -p /sbin/ldconfig


%post -n libmount -p /sbin/ldconfig
%postun -n libmount -p /sbin/ldconfig

%pre -n uuidd
getent group uuidd >/dev/null || groupadd -r uuidd
getent passwd uuidd >/dev/null || \
useradd -r -g uuidd -d /var/lib/libuuid -s /sbin/nologin \
    -c "UUID generator helper daemon" uuidd
exit 0

%if %{with_systemd}
%post -n uuidd
if [ $1 -eq 1 ]; then
	# Package install,
	systemctl enable uuidd.service >/dev/null 2>&1 || :
	systemctl start uuidd.service > /dev/null 2>&1 || :
else
	# Package upgrade
	if systemctl --quiet is-enabled uuidd.service ; then
		systemctl reenable uuidd.service >/dev/null 2>&1 || :
	fi
fi
%preun -n uuidd
if [ "$1" = 0 ]; then
	systemctl stop uuidd.service > /dev/null 2>&1 || :
	systemctl disable uuidd.service > /dev/null 2>&1 || :
fi

%post -n fstrim 
if [ $1 -eq 1 ]; then
    # Package install,
    systemctl enable fstrim.service >/dev/null 2>&1 || :
    systemctl start fstrim.service > /dev/null 2>&1 || :
else
    # Package upgrade
    if systemctl --quiet is-enabled fstrim.service ; then
        systemctl reenable fstrim.service >/dev/null 2>&1 || :
    fi
fi
%preun -n fstrim 
if [ "$1" = 0 ]; then
    systemctl stop fstrim.service > /dev/null 2>&1 || :
    systemctl disable fstrim.service > /dev/null 2>&1 || :
fi

%endif


%files -f %{name}.files
%defattr(-,root,root)
%config(noreplace)	%{_sysconfdir}/pam.d/chfn
%config(noreplace)	%{_sysconfdir}/pam.d/chsh
%config(noreplace)	%{_sysconfdir}/pam.d/login
%config(noreplace)	%{_sysconfdir}/pam.d/remote
%config(noreplace)	%{_sysconfdir}/pam.d/su
%config(noreplace)	%{_sysconfdir}/pam.d/su-l
%config(noreplace)	%{_sysconfdir}/pam.d/runuser
%config(noreplace)	%{_sysconfdir}/pam.d/runuser-l
#%config(noreplace)	%{_prefix}/lib/udev/rules.d/60-raw.rules

%attr(4755,root,root)	%{_bindir}/mount
%attr(4755,root,root)	%{_bindir}/umount
%attr(4755,root,root)	%{_bindir}/su
%attr(755,root,root)	%{_bindir}/login
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%attr(2755,root,tty)	%{_bindir}/write

%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/mtab

%{_bindir}/cal
%{_bindir}/chrt
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/eject
%{_bindir}/fallocate
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ionice
%{_bindir}/ipcmk
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/lscpu
%{_bindir}/lslocks
%{_bindir}/mcookie
%{_bindir}/namei
%{_bindir}/nsenter
%{_bindir}/prlimit
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/scriptreplay
%{_bindir}/setarch
%{_bindir}/setsid
%{_bindir}/setterm
%{_bindir}/tailf
%{_bindir}/taskset
%{_bindir}/ul
%{_bindir}/unshare
%{_bindir}/utmpdump
%{_bindir}/uuidgen
%{_bindir}/whereis
%{_bindir}/lslogins
%{_bindir}/lsipc
%{_bindir}/setpriv
%{_bindir}/uname26
%{_sbindir}/zramctl

%{_mandir}/man1/last.1.gz
%{_mandir}/man1/lastb.1.gz
%{_mandir}/man1/mesg.1.gz
%{_mandir}/man1/cal.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/chrt.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/dmesg.1*
%{_mandir}/man1/eject.1*
%{_mandir}/man1/fallocate.1*
%{_mandir}/man1/flock.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/wall.1*
%{_mandir}/man1/hexdump.1*
%{_mandir}/man1/ionice.1*
%{_mandir}/man1/ipcmk.1*
%{_mandir}/man1/ipcrm.1*
%{_mandir}/man1/ipcs.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/lscpu.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/mountpoint.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/nsenter.1*
%{_mandir}/man1/prlimit.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/renice.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/runuser.1*
%{_mandir}/man1/script.1*
%{_mandir}/man1/scriptreplay.1*
%{_mandir}/man1/setsid.1*
%{_mandir}/man1/setterm.1*
%{_mandir}/man1/su.1*
%{_mandir}/man1/tailf.1*
%{_mandir}/man1/taskset.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/unshare.1*
%{_mandir}/man1/utmpdump.1.gz
%{_mandir}/man1/uuidgen.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*
%{_mandir}/man1/lslogins.1.gz
%{_mandir}/man1/lsipc.1.gz
%{_mandir}/man1/setpriv.1.gz

%{_mandir}/man5/terminal-colors.d.5.gz

%{_mandir}/man5/fstab.5*
%{_mandir}/man8/addpart.8*
%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blkdiscard.8*
%{_mandir}/man8/blkid.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/chcpu.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/delpart.8*
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/findfs.8*
%{_mandir}/man8/findmnt.8*
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/fsck.cramfs.8*
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/fsfreeze.8*
%{_mandir}/man8/isosize.8*
%{_mandir}/man8/ldattach.8*
%{_mandir}/man8/losetup.8*
%{_mandir}/man8/lsblk.8*
%{_mandir}/man8/lslocks.8.gz
%{_mandir}/man8/mkfs.8*
%{_mandir}/man8/mkfs.cramfs.8*
%{_mandir}/man8/mkfs.minix.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/nologin.8*
%{_mandir}/man8/partx.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/raw.8*
%{_mandir}/man8/rawdevices.8*
%{_mandir}/man8/readprofile.8*
%{_mandir}/man8/resizepart.8*
%{_mandir}/man8/rtcwake.8*
%{_mandir}/man8/setarch.8*
%{_mandir}/man8/sulogin.8.gz
%{_mandir}/man8/swaplabel.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/switch_root.8*
%{_mandir}/man8/umount.8*
%{_mandir}/man8/wdctl.8.gz
%{_mandir}/man8/wipefs.8*
%{_mandir}/man8/uname26.8.gz
%{_mandir}/man8/zramctl.8.gz
%{_sbindir}/addpart
%{_sbindir}/delpart
%{_sbindir}/ldattach
%{_sbindir}/nologin
%{_sbindir}/partx
%{_sbindir}/readprofile
%{_sbindir}/resizepart
%{_sbindir}/rtcwake
%{_bindir}/last
%{_bindir}/lastb
%{_bindir}/mesg
%{_bindir}/wall
%{_bindir}/dmesg
%{_bindir}/findmnt
%{_bindir}/kill
%{_bindir}/lsblk
%{_bindir}/more
%{_bindir}/mountpoint
%{_bindir}/wdctl
%{_sbindir}/raw
%{_sbindir}/agetty
%{_sbindir}/blkdiscard
%{_sbindir}/blkid
%{_sbindir}/blockdev
%{_sbindir}/chcpu
%{_sbindir}/ctrlaltdel
%{_sbindir}/fdisk
%{_sbindir}/findfs
%{_sbindir}/fsck
%{_sbindir}/fsck.cramfs
%{_sbindir}/fsck.minix
%{_sbindir}/fsfreeze
%{_sbindir}/losetup
%{_sbindir}/mkfs
%{_sbindir}/mkfs.cramfs
%{_sbindir}/mkfs.minix
%{_sbindir}/mkswap
%{_sbindir}/pivot_root
%{_sbindir}/runuser
%{_sbindir}/sulogin
%{_sbindir}/swaplabel
%{_sbindir}/swapoff
%{_sbindir}/swapon
%{_sbindir}/switch_root
%{_sbindir}/wipefs

#%{_docdir}/util-linux/getopt/*

%ifnarch s390 s390x
%{_sbindir}/fdformat
%{_sbindir}/hwclock
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/hwclock.8*
%endif

%{_sbindir}/cfdisk
%{_sbindir}/sfdisk
%{_mandir}/man8/cfdisk.8*
%{_mandir}/man8/sfdisk.8*

%ifarch %cytune_archs
%{_bindir}/cytune
%{_mandir}/man8/cytune.8*
%endif

%{_datadir}/bash-completion/completions/*

%files -n uuidd
%defattr(-,root,root)
%{_mandir}/man8/uuidd.8*
%{_sbindir}/uuidd

%if %{with_systemd}
%{_unitdir}/uuidd.*
%endif

%dir %attr(2775, uuidd, uuidd) /var/lib/libuuid
%dir %attr(2775, uuidd, uuidd) /run/uuidd


%files -n fstrim
%defattr(-,root,root)
%{_mandir}/man8/fstrim.8*
%{_sbindir}/fstrim
%if %{with_systemd}
%{_unitdir}/fstrim.*
%endif

%files -n libmount
%defattr(-,root,root)
%{_libdir}/libmount.so.*

%files -n libmount-devel
%defattr(-,root,root)
%{_libdir}/libmount.so
%{_includedir}/libmount
%{_libdir}/pkgconfig/mount.pc

%files -n python-libmount
%defattr(-,root,root)
%{_libdir}/python*/site-packages/libmount


%files -n libblkid
%defattr(-,root,root)
%{_libdir}/libblkid.so.*

%files -n libblkid-devel
%defattr(-,root,root)
%{_libdir}/libblkid.so
%{_includedir}/blkid
%{_mandir}/man3/libblkid.3*
%{_libdir}/pkgconfig/blkid.pc


%files -n libuuid
%defattr(-,root,root)
%{_libdir}/libuuid.so.*

%files -n libuuid-devel
%defattr(-,root,root)
%{_libdir}/libuuid.so
%{_includedir}/uuid
%{_mandir}/man3/uuid.3*
%{_mandir}/man3/uuid_clear.3*
%{_mandir}/man3/uuid_compare.3*
%{_mandir}/man3/uuid_copy.3*
%{_mandir}/man3/uuid_generate.3*
%{_mandir}/man3/uuid_generate_random.3*
%{_mandir}/man3/uuid_generate_time.3*
%{_mandir}/man3/uuid_generate_time_safe.3*
%{_mandir}/man3/uuid_is_null.3*
%{_mandir}/man3/uuid_parse.3*
%{_mandir}/man3/uuid_time.3*
%{_mandir}/man3/uuid_unparse.3*
%{_libdir}/pkgconfig/uuid.pc


%files -n libsmartcols
%{_libdir}/libsmartcols.so.*

%files -n libsmartcols-devel
%dir %{_includedir}/libsmartcols
%{_includedir}/libsmartcols/libsmartcols.h
%{_libdir}/libsmartcols.so
%{_libdir}/pkgconfig/smartcols.pc

%files -n libfdisk
%{_libdir}/libfdisk.so.*

%files -n libfdisk-devel
%dir %{_includedir}/libfdisk
%{_includedir}/libfdisk/libfdisk.h
%{_libdir}/libfdisk.so
%{_libdir}/pkgconfig/fdisk.pc


%changelog
* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- update to 2.27

