
#the package contains pkg-config files, but DO NOT let it depend on pkgconfig
%global __requires_exclude pkg-config

%global enable_terminal 1 

Name:           systemd
Url:            http://www.freedesktop.org/wiki/Software/systemd
Version:        227
Release:        6
License:        LGPLv2+ and MIT and GPLv2+
Summary:        A System and Service Manager
Source0:        http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.gz
Source1:        90-default.preset
Source5:        85-display-manager.preset
Source7:        99-default-disable.preset

# Prevent accidental removal of the systemd package
Source10:        yum-protect-systemd.conf

Patch0: systemd-fix-logind-failed-upstream-issue-1505.patch

BuildRequires:  glib2-devel
BuildRequires:  pciutils-devel
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  pam-devel
BuildRequires:  audit-libs-devel
BuildRequires:  dbus-devel
BuildRequires:  libacl-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libblkid-devel
BuildRequires:  xz-devel
BuildRequires:  libcurl-devel
BuildRequires:  kmod-devel
BuildRequires:  libelfutils-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  gnutls-devel
BuildRequires:  iptables-devel
BuildRequires:  bzip2-devel
BuildRequires:  lz4-devel
BuildRequires:  lz4-static
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  pkgconfig
BuildRequires:  intltool
BuildRequires:  gperf
BuildRequires:  gawk
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
%ifarch %{ix86} x86_64
BuildRequires:  gnu-efi gnu-efi-devel
%endif

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

#for test-path-util fsck.minix
BuildRequires:  util-linux

%if %enable_terminal
BuildRequires:  libxkbcommon-devel
%endif

Requires(post): coreutils
Requires(post): gawk
Requires(post): sed
Requires(post): acl
Requires(pre):  coreutils
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/groupadd
Requires:       dbus
Requires:       %{name}-libs = %{version}-%{release}

Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       syslog
Provides:       systemd-units = %{version}-%{release}
# part of system since f18, drop at f20
Provides:       udev = %{version}
Obsoletes:      udev < 183
Conflicts:      dracut < 027
# f18 version, drop at f20
Conflicts:      plymouth < 0.8.5.1
# Ensures correct multilib updates added F18, drop at F20
Obsoletes:      systemd < 185-4
Conflicts:      systemd < 185-4
# added F18, drop at F20
Obsoletes:      system-setup-keyboard < 0.9
Provides:       system-setup-keyboard = 0.9
# systemd-analyze got merged in F19, drop at F21
Obsoletes:      systemd-analyze < 198
Provides:       systemd-analyze = 198

%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT

%description libs
Libraries for systemd and udev, as well as the systemd PAM module.

%package devel
Summary:        Development headers for systemd
License:        LGPLv2+ and MIT
Requires:       %{name} = %{version}-%{release}
Provides:       libudev-devel = %{version}

%description devel
Development headers and auxiliary files for developing applications for systemd.

%package -n libgudev1
Summary:        Libraries for adding libudev support to applications that use glib
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}

%description -n libgudev1
This package contains the libraries that make it easier to use libudev
functionality from applications that use glib.

%package -n libgudev1-devel
Summary:        Header files for adding libudev support to applications that use glib
Requires:       libgudev1 = %{version}-%{release}
License:        LGPLv2+

%description -n libgudev1-devel
This package contains the header and pkg-config files for developing
glib-based applications using libudev functionality.

%prep
%setup -q
%patch0 -p1

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
        --libexecdir=%{_prefix}/lib \
        --enable-compat-libs \
        --enable-myhostname \
        --enable-machined \
        --enable-networkd \
	--enable-manpages \
        --enable-resolved \
        --enable-libcurl \
        --disable-gtk-doc \
        --disable-static \
        --disable-qrencode \
        --disable-ima \
        --disable-kdbus \
        --disable-microhttpd \
        --disable-libidn \
        --disable-sysusers \
        --disable-selinux \
        --enable-smack \
        --enable-lz4 \
        --enable-audit \
        --enable-polkit \
%if %enable_terminal
        --enable-terminal \
%else
        --disable-terminal \
%endif
        --enable-tests \
	--with-ntp-servers="asia.pool.ntp.org 0.asia.pool.ntp.org 1.asia.pool.ntp.org 2.asia.pool.ntp.org 3.asia.pool.ntp.org 0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org" \
	--with-certificate-root=/etc/pki/tls \
        --with-sysvinit-path=/etc/rc.d/init.d \
        --with-rc-local-script-path-start=/etc/rc.d/rc.local \
        --enable-introspection=no \
        PYTHON=%{__python3}
        
#-fno-lto to fix compile with gcc-4.9
make CFLAGS="${CFLAGS} -fno-lto" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install yum protection fragment
install -Dm0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/yum/protected.d/systemd.conf

find %{buildroot} \( -name '*.a' -o -name '*.la' \) -delete

#put rpm macros in /etc
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rpm
install -m 0644 src/core/macros.systemd $RPM_BUILD_ROOT/%{_sysconfdir}/rpm/macros.systemd
rm -rf $RPM_BUILD_ROOT/%{_libdir}/rpm

# udev links
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
ln -s ../lib/systemd/systemd %{buildroot}%{_sbindir}/init
ln -s ../lib/systemd/systemd %{buildroot}%{_bindir}/systemd
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/reboot
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/halt
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/poweroff
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/shutdown
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/telinit
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/runlevel

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/basic.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/default.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/dbus.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/syslog.target.wants

# Temporary workaround for #1002806
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/poweroff.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/rescue.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/multi-user.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/graphical.target.wants
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/reboot.target.wants
ln -s ../systemd-update-utmp-runlevel.service %{buildroot}%{_prefix}/lib/systemd/system/poweroff.target.wants/
ln -s ../systemd-update-utmp-runlevel.service %{buildroot}%{_prefix}/lib/systemd/system/reboot.target.wants/

# Make sure the user generators dir exists too
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-generators
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-generators

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/localtime
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf

# Install default preset policy
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system-preset/

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-shutdown/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-sleep/

# Make sure the NTP units dir exists
mkdir -p %{buildroot}%{_prefix}/lib/systemd/ntp-units.d/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/log/journal

touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin

rm -f %{buildroot}%{_prefix}/lib/sysctl.d/50-coredump.conf

# For now remove /var/log/README since we are not enabling persistant
# logging yet.
rm -f %{buildroot}%{_localstatedir}/log/README

%check
#make check in koji will hang.
#please make check in native machine before update.
#make check ||:


%pre
getent group cdrom >/dev/null 2>&1 || groupadd -r -g 11 cdrom >/dev/null 2>&1 || :
getent group input >/dev/null 2>&1 || groupadd -r input >/dev/null 2>&1 || :
getent group tape >/dev/null 2>&1 || groupadd -r -g 33 tape >/dev/null 2>&1 || :
getent group dialout >/dev/null 2>&1 || groupadd -r -g 18 dialout >/dev/null 2>&1 || :
getent group floppy >/dev/null 2>&1 || groupadd -r -g 19 floppy >/dev/null 2>&1 || :
getent group systemd-journal >/dev/null 2>&1 || groupadd -r -g 190 systemd-journal 2>&1 || :

getent group systemd-timesync >/dev/null 2>&1 || groupadd -r systemd-timesync 2>&1 || :
getent passwd systemd-timesync >/dev/null 2>&1 || useradd -r -l -g systemd-timesync -d / -s /usr/sbin/nologin -c "Systemd Timesync" systemd-timesync >/dev/null 2>&1 || :
getent group systemd-network >/dev/null 2>&1 || groupadd -r systemd-network 2>&1 || :
getent passwd systemd-network >/dev/null 2>&1 || useradd -r -l -g systemd-network -d / -s /usr/sbin/nologin -c "Systemd Network" systemd-network >/dev/null 2>&1 || :
getent group systemd-resolve >/dev/null 2>&1 || groupadd -r systemd-resolve 2>&1 || :
getent passwd systemd-resolve >/dev/null 2>&1 || useradd -r -l -g systemd-resolve -d / -s /usr/sbin/nologin -c "Systemd Resolve" systemd-resolve >/dev/null 2>&1 || :
getent group systemd-bus-proxy >/dev/null 2>&1 || groupadd -r systemd-bus-proxy 2>&1 || :
getent passwd systemd-bus-proxy >/dev/null 2>&1 || useradd -r -l -g systemd-bus-proxy -d / -s /usr/sbin/nologin -c "Systemd Bus Proxy" systemd-bus-proxy >/dev/null 2>&1 || :

getent group systemd-journal-gateway >/dev/null 2>&1 || groupadd -r -g 191 systemd-journal-gateway 2>&1 || :
getent group systemd-journal-remote >/dev/null 2>&1 || groupadd -r -g 192 systemd-journal-remote 2>&1 || :
getent passwd systemd-journal-gateway >/dev/null 2>&1 || useradd -r -l -u 191 -g systemd-journal-gateway -d %{_localstatedir}/log/journal -s /usr/sbin/nologin -c "Journal Gateway" systemd-journal-gateway >/dev/null 2>&1 || :

systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :


%post
systemd-machine-id-setup >/dev/null 2>&1 || :
/usr/lib/systemd/systemd-random-seed save >/dev/null 2>&1 || :
systemctl daemon-reexec >/dev/null 2>&1 || :
systemctl start systemd-udevd.service >/dev/null 2>&1 || :
udevadm hwdb --update >/dev/null 2>&1 || :
journalctl --update-catalog >/dev/null 2>&1 || :
systemd-tmpfiles --create >/dev/null 2>&1 || :

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :
chmod g+s /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ >/dev/null 2>&1 || :


# Services we install by default, and which are controlled by presets.
if [ $1 -eq 1 ] ; then
        systemctl preset \
                getty@tty1.service \
                remote-fs.target \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                >/dev/null 2>&1 || :
fi

# sed-fu to add myhostname to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' /etc/nsswitch.conf >/dev/null 2>&1 || :
fi

%systemd_post systemd-journal-gatewayd.socket systemd-journal-gatewayd.service

%preun
if [ $1 -eq 0 ] ; then
        systemctl disable \
                getty@.service \
                remote-fs.target \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                >/dev/null 2>&1 || :

        rm -f /etc/systemd/system/default.target >/dev/null 2>&1 || :

        if [ -f /etc/nsswitch.conf ] ; then
                sed -i.bak -e '
                        /^hosts:/ !b
                        s/[[:blank:]]\+myhostname\>//
                        ' /etc/nsswitch.conf >/dev/null 2>&1 || :
        fi
fi

%systemd_preun systemd-journal-gatewayd.socket systemd-journal-gatewayd.service

%postun
if [ $1 -ge 1 ] ; then
        systemctl daemon-reload > /dev/null 2>&1 || :
        systemctl try-restart systemd-logind.service >/dev/null 2>&1 || :
fi
%systemd_postun_with_restart systemd-journal-gatewayd.service


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post -n libgudev1 -p /sbin/ldconfig
%postun -n libgudev1 -p /sbin/ldconfig

%files
%doc %{_docdir}/systemd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/systemd-user
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/udev/udev.conf

%{_sysconfdir}/yum/protected.d/systemd.conf

%ghost %{_sysconfdir}/udev/hwdb.bin
%{_sysconfdir}/rpm/macros.systemd
%{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rc.d/init.d/README
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh

%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/localtime
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%{_bindir}/*
%dir %{_libdir}/systemd
%{_libdir}/systemd/*
%dir %{_datadir}/systemd
%dir %{_datadir}/pkgconfig
%dir %{_localstatedir}/log/journal
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%dir %{_localstatedir}/lib/systemd/coredump
%ghost %{_localstatedir}/lib/systemd/catalog/database

%caps(cap_dac_override,cap_sys_ptrace=pe) %{_bindir}/systemd-detect-virt
%{_prefix}/lib/udev
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/tmpfiles.d/legacy.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_prefix}/lib/tmpfiles.d/journal-nocow.conf
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth

%{_prefix}/lib/sysctl.d/50-default.conf
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%{_prefix}/lib/systemd/catalog/systemd.catalog
%{_prefix}/lib/kernel/install.d/50-depmod.install
%{_prefix}/lib/kernel/install.d/90-loaderentry.install
%{_sbindir}/init
%{_sbindir}/reboot
%{_sbindir}/halt
%{_sbindir}/poweroff
%{_sbindir}/shutdown
%{_sbindir}/telinit
%{_sbindir}/runlevel
%{_sbindir}/udevadm
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_datadir}/dbus-1/*
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
%{_datadir}/bash-completion/completions/*
%{_datadir}/zsh/site-functions/*
%if %enable_terminal
#%{_datadir}/systemd/unifont-glyph-array.bin
%endif

%{_libdir}/security/pam_systemd.so

%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/locale/*/LC_MESSAGES/systemd.mo


%files libs
%{_libdir}/libnss_myhostname.so.2
%{_libdir}/libnss_mymachines.so.2
%{_libdir}/libnss_resolve.so.2
%{_libdir}/libudev.so.*
%{_libdir}/libsystemd.so.*
%{_libdir}/libsystemd-*.so.*

%files devel
%dir %{_includedir}/systemd
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_libdir}/libsystemd-*.so
%{_includedir}/systemd/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 227-6
- Enable lz4

* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 227-5
- Bump version

* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 227-4
- Add yum protect config file, fix build requires

* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 227-3
- Fix 1505 issue, logind failed sometimes

* Fri Oct 23 2015 cjacker - 227-2
- Rebuild for new 4.0 release

* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- update to 227

