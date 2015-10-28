Summary:     The mdadm program controls Linux md devices (software RAID arrays)
Name:        mdadm
Version:     3.3.2
Release:     2%{?dist}
Source:      http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.xz
Source1:     mdmonitor.init
Source2:     raid-check
Source3:     mdadm.rules
Source4:     mdadm-raid-check-sysconfig
Source5:     mdadm-cron
Source6:     mdmonitor.service
Source7:     mdadm.conf
#Source8:     mdadm_event.conf

# Fedora customization patches
Patch97:     mdadm-3.3-udev.patch
Patch98:     mdadm-2.5.2-static.patch
URL:         http://www.kernel.org/pub/linux/utils/raid/mdadm/
License:     GPLv2+
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:   mdctl,raidtools
Conflicts:   dracut < 034-1
Requires(post): systemd-units coreutils
BuildRequires: systemd-units binutils-devel
Requires(preun): systemd-units
Requires(postun): systemd-units coreutils
#Requires: libreport-filesystem

%description 
The mdadm program is used to create, manage, and monitor Linux MD (software
RAID) devices.  As such, it provides similar functionality to the raidtools
package.  However, mdadm is a single program, and it can perform
almost all functions without a configuration file, though a configuration
file can be used to help with some common tasks.

%prep
%setup -q

# Fedora customization patches
%patch97 -p1 -b .udev
%patch98 -p1 -b .static

%build
make %{?_smp_mflags} CXFLAGS="$RPM_OPT_FLAGS" SYSCONFDIR="%{_sysconfdir}" mdadm mdmon

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_sbindir} SYSTEMD_DIR=%{_unitdir} install install-systemd
install -Dp -m 755 %{SOURCE2} %{buildroot}%{_sbindir}/raid-check
install -Dp -m 644 %{SOURCE3} %{buildroot}%{_udevrulesdir}/65-md-incremental.rules
install -Dp -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -Dp -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.d/raid-check
mkdir -p -m 710 %{buildroot}/var/run/mdadm

# systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE6} %{buildroot}%{_unitdir}

# tmpfile
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE7} %{buildroot}%{_tmpfilesdir}/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/%{name}/

# abrt
#mkdir -p %{buildroot}/etc/libreport/events.d
#install -m644 %{SOURCE8} %{buildroot}/etc/libreport/events.d

%clean
rm -rf %{buildroot}

%post
%systemd_post mdmonitor.service
/usr/bin/systemctl disable mdmonitor-takeover.service  >/dev/null 2>&1 || :

%preun
%systemd_preun mdmonitor.service

%postun
%systemd_postun_with_restart mdmonitor.service

%files
%defattr(-,root,root,-)
%doc TODO ChangeLog mdadm.conf-example COPYING misc/*
%{_udevrulesdir}/*
%{_sbindir}/*
%{_unitdir}/*
%{_mandir}/man*/md*
/usr/lib/systemd/system-shutdown/*
%config(noreplace) %{_sysconfdir}/cron.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
%dir %{_localstatedir}/run/%{name}/
%config(noreplace) %{_tmpfilesdir}/%{name}.conf
#/etc/libreport/events.d/*

%changelog
* Fri Oct 23 2015 cjacker - 3.3.2-2
- Rebuild for new 4.0 release

