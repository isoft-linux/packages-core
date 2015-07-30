%define device_mapper_version 1.02.93

%define enable_cache 1
%define enable_cluster 0 
%define enable_cmirror 0
%define enable_lvmetad 1
%define enable_python 1
%define enable_thin 1

%define systemd_version 189-3
%define dracut_version 002-18
%define util_linux_version 2.24
%define bash_version 4.0
%define corosync_version 1.99.9-1
%define resource_agents_version 3.9.5-12
%define dlm_version 3.99.1-1
%define persistent_data_version 0.3.2-1

%if %{enable_cluster}
  %define configure_cluster --with-cluster=internal --with-clvmd=corosync
  %if %{enable_cmirror}
    %define configure_cmirror --enable-cmirrord
  %endif
%else
    %define configure_cluster --with-cluster=internal --with-clvmd=none
%endif


# Do not reset Release to 1 unless both lvm2 and device-mapper 
# versions are increased together.

Summary: Userland logical volume management tools 
Name: lvm2
Version: 2.02.116
Release: 3%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://sources.redhat.com/lvm2
Source0: ftp://sources.redhat.com/pub/lvm2/releases/LVM2.%{version}.tgz
Patch0: lvm2-set-default-preferred_names.patch
Patch1: lvm2-enable-lvmetad-by-default.patch
Patch2: lvm2-remove-mpath-device-handling-from-udev-rules.patch

BuildRequires: libblkid-devel >= %{util_linux_version}
BuildRequires: ncurses-devel
BuildRequires: readline-devel
%if %{enable_cluster}
BuildRequires: corosynclib-devel >= %{corosync_version}
BuildRequires: dlm-devel >= %{dlm_version}
%endif
BuildRequires: module-init-tools
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: systemd-units
%if %{enable_python}
BuildRequires: python2-devel
BuildRequires: python-setuptools
%endif
%if %{enable_thin} || %{enable_cache}
BuildRequires: device-mapper-persistent-data >= %{persistent_data_version}
%endif
Requires: %{name}-libs = %{version}-%{release}
Requires: bash >= %{bash_version}
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}
Requires: module-init-tools
%if %{enable_thin} || %{enable_cache}
Requires: device-mapper-persistent-data >= %{persistent_data_version}
%endif

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .preferred_names
%patch1 -p1 -b .enable_lvmetad
%patch2 -p1 -b .udev_no_mpath

%build
%define _default_pid_dir /run
%define _default_dm_run_dir /run
%define _default_run_dir /run/lvm
%define _default_locking_dir /run/lock/lvm

%define _udevdir %{_prefix}/lib/udev/rules.d
%define _tmpfilesdir %{_prefix}/lib/tmpfiles.d

%define configure_udev --with-udevdir=%{_udevdir} --enable-udev_sync

%if %{enable_cache}
%define configure_cache --with-cache=internal
%endif

%if %{enable_thin}
%define configure_thin --with-thin=internal
%endif

%if %{enable_lvmetad}
%define configure_lvmetad --enable-lvmetad
%endif

%if %{enable_python}
%define configure_python --enable-python-bindings
%endif

%configure --with-default-dm-run-dir=%{_default_dm_run_dir} --with-default-run-dir=%{_default_run_dir} --with-default-pid-dir=%{_default_pid_dir} --with-default-locking-dir=%{_default_locking_dir} --with-usrlibdir=%{_libdir} --enable-lvm1_fallback --enable-fsadm --with-pool=internal --enable-write_install --with-user= --with-group= --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-pkgconfig --enable-applib --enable-cmdlib --enable-dmeventd --enable-blkid_wiping %{?configure_python} %{?configure_cluster} %{?configure_cmirror} %{?configure_udev} %{?configure_thin} %{?configure_lvmetad} %{?configure_cache}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
make install_system_dirs DESTDIR=$RPM_BUILD_ROOT
make install_systemd_units DESTDIR=$RPM_BUILD_ROOT
make install_systemd_generators DESTDIR=$RPM_BUILD_ROOT
make install_tmpfiles_configuration DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post blk-availability.service lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_post lvm2-lvmetad.socket
%endif

%preun
%systemd_preun blk-availability.service lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_preun lvm2-lvmetad.service lvm2-lvmetad.socket
%endif

%postun
%systemd_postun lvm2-monitor.service
%if %{enable_lvmetad}
%systemd_postun_with_restart lvm2-lvmetad.service
%endif

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%doc README VERSION WHATS_NEW
%doc doc/lvm_fault_handling.txt

# Main binaries
%defattr(555,root,root,-)
%{_sbindir}/blkdeactivate
%{_sbindir}/fsadm
%{_sbindir}/lvm
%{_sbindir}/lvmconf
%{_sbindir}/lvmdump
%if %{enable_lvmetad}
%{_sbindir}/lvmetad
%endif
%{_sbindir}/vgimportclone

# Other files
%defattr(444,root,root,-)
%{_sbindir}/lvchange
%{_sbindir}/lvconvert
%{_sbindir}/lvcreate
%{_sbindir}/lvdisplay
%{_sbindir}/lvextend
%{_sbindir}/lvmchange
%{_sbindir}/lvmdiskscan
%{_sbindir}/lvmsadc
%{_sbindir}/lvmsar
%{_sbindir}/lvreduce
%{_sbindir}/lvremove
%{_sbindir}/lvrename
%{_sbindir}/lvresize
%{_sbindir}/lvs
%{_sbindir}/lvscan
%{_sbindir}/pvchange
%{_sbindir}/pvck
%{_sbindir}/pvcreate
%{_sbindir}/pvdisplay
%{_sbindir}/pvmove
%{_sbindir}/pvremove
%{_sbindir}/pvresize
%{_sbindir}/pvs
%{_sbindir}/pvscan
%{_sbindir}/vgcfgbackup
%{_sbindir}/vgcfgrestore
%{_sbindir}/vgchange
%{_sbindir}/vgck
%{_sbindir}/vgconvert
%{_sbindir}/vgcreate
%{_sbindir}/vgdisplay
%{_sbindir}/vgexport
%{_sbindir}/vgextend
%{_sbindir}/vgimport
%{_sbindir}/vgmerge
%{_sbindir}/vgmknodes
%{_sbindir}/vgreduce
%{_sbindir}/vgremove
%{_sbindir}/vgrename
%{_sbindir}/vgs
%{_sbindir}/vgscan
%{_sbindir}/vgsplit
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lvmcache.7.gz
%{_mandir}/man7/lvmthin.7.gz
%{_mandir}/man8/blkdeactivate.8.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lvchange.8.gz
%{_mandir}/man8/lvconvert.8.gz
%{_mandir}/man8/lvcreate.8.gz
%{_mandir}/man8/lvdisplay.8.gz
%{_mandir}/man8/lvextend.8.gz
%{_mandir}/man8/lvm.8.gz
%{_mandir}/man8/lvm2-activation-generator.8.gz
%{_mandir}/man8/lvm-dumpconfig.8.gz
%{_mandir}/man8/lvmchange.8.gz
%{_mandir}/man8/lvmconf.8.gz
%{_mandir}/man8/lvmdiskscan.8.gz
%{_mandir}/man8/lvmdump.8.gz
%{_mandir}/man8/lvmsadc.8.gz
%{_mandir}/man8/lvmsar.8.gz
%{_mandir}/man8/lvreduce.8.gz
%{_mandir}/man8/lvremove.8.gz
%{_mandir}/man8/lvrename.8.gz
%{_mandir}/man8/lvresize.8.gz
%{_mandir}/man8/lvs.8.gz
%{_mandir}/man8/lvscan.8.gz
%{_mandir}/man8/pvchange.8.gz
%{_mandir}/man8/pvck.8.gz
%{_mandir}/man8/pvcreate.8.gz
%{_mandir}/man8/pvdisplay.8.gz
%{_mandir}/man8/pvmove.8.gz
%{_mandir}/man8/pvremove.8.gz
%{_mandir}/man8/pvresize.8.gz
%{_mandir}/man8/pvs.8.gz
%{_mandir}/man8/pvscan.8.gz
%{_mandir}/man8/vgcfgbackup.8.gz
%{_mandir}/man8/vgcfgrestore.8.gz
%{_mandir}/man8/vgchange.8.gz
%{_mandir}/man8/vgck.8.gz
%{_mandir}/man8/vgconvert.8.gz
%{_mandir}/man8/vgcreate.8.gz
%{_mandir}/man8/vgdisplay.8.gz
%{_mandir}/man8/vgexport.8.gz
%{_mandir}/man8/vgextend.8.gz
%{_mandir}/man8/vgimport.8.gz
%{_mandir}/man8/vgimportclone.8.gz
%{_mandir}/man8/vgmerge.8.gz
%{_mandir}/man8/vgmknodes.8.gz
%{_mandir}/man8/vgreduce.8.gz
%{_mandir}/man8/vgremove.8.gz
%{_mandir}/man8/vgrename.8.gz
%{_mandir}/man8/vgs.8.gz
%{_mandir}/man8/vgscan.8.gz
%{_mandir}/man8/vgsplit.8.gz
%{_udevdir}/11-dm-lvm.rules
%if %{enable_lvmetad}
%{_mandir}/man8/lvmetad.8.gz
%{_udevdir}/69-dm-lvm-metad.rules
%endif
%dir %{_sysconfdir}/lvm
%ghost %{_sysconfdir}/lvm/cache/.cache
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/command_profile_template.profile
%{_sysconfdir}/lvm/profile/metadata_profile_template.profile
%{_sysconfdir}/lvm/profile/thin-generic.profile
%{_sysconfdir}/lvm/profile/thin-performance.profile
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%ghost %dir %{_default_locking_dir}
%ghost %dir %{_default_run_dir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%attr(555, -, -) %{_prefix}/lib/systemd/system-generators/lvm2-activation-generator
%if %{enable_lvmetad}
%{_unitdir}/lvm2-lvmetad.socket
%{_unitdir}/lvm2-lvmetad.service
%{_unitdir}/lvm2-pvscan@.service
%endif

##############################################################################
# Library and Development subpackages
##############################################################################
%package devel
Summary: Development libraries and headers
Group: Development/Libraries
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires: device-mapper-devel = %{device_mapper_version}-%{release}
Requires: device-mapper-event-devel = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%files devel
%defattr(444,root,root,-)
%{_libdir}/liblvm2app.so
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2app.h
%{_includedir}/lvm2cmd.h
%{_libdir}/pkgconfig/lvm2app.pc

%package libs
Summary: Shared libraries for lvm2
License: LGPLv2
Group: System Environment/Libraries
Requires: device-mapper-event = %{device_mapper_version}-%{release}

%description libs
This package contains shared lvm2 libraries for applications.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(555,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%{_libdir}/liblvm2app.so.*
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so

%if %{enable_thin}
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%endif

%if %{enable_python}

%package python-libs
Summary: Python module to access LVM
License: LGPLv2
Group: Development/Libraries
Provides: python-lvm = %{version}-%{release}
Obsoletes: python-lvm < 2.02.98-2
Requires: %{name}-libs = %{version}-%{release}

%description python-libs
Python module to allow the creation and use of LVM
logical volumes, physical volumes, and volume groups.

%files python-libs
%{python_sitearch}/*

%endif

##############################################################################
# Cluster subpackage
# The 'clvm' OCF script to manage clvmd instance is part of resource-agents.
##############################################################################
%if %{enable_cluster}

%package cluster
Summary: Cluster extensions for userland logical volume management tools
License: GPLv2
Group: System Environment/Base
Requires: lvm2 = %{version}-%{release}
Requires(preun): device-mapper >= %{device_mapper_version}
Requires(preun): lvm2 >= 2.02
Requires: corosync >= %{corosync_version}
Requires: dlm >= %{dlm_version}
Requires: resource-agents >= %{resource_agents_version}

%description cluster

Extensions to LVM2 to support clusters.

%post cluster
if [ -e %{_default_pid_dir}/clvmd.pid ]; then
	/usr/sbin/clvmd -S || echo "Failed to restart clvmd daemon. Please, try manual restart."
fi

%preun cluster
if [ "$1" = "0" ]; then
	/sbin/lvmconf --disable-cluster
fi

%files cluster
%defattr(555,root,root,-)
%{_sbindir}/clvmd
%attr(444, -, -) %{_mandir}/man8/clvmd.8.gz

##############################################################################
# Cluster-standalone subpackage
##############################################################################
%package cluster-standalone
Summary: Additional files to support clustered LVM2 in standalone mode
License: GPLv2
Group: System Environment/Base
Requires: lvm2-cluster = %{version}-%{release}

%description cluster-standalone

Additional files needed to run clustered LVM2 daemon and clustered volume
activation in standalone mode as services without cluster resource manager
involvement (e.g. pacemaker).

%post cluster-standalone
%systemd_post lvm2-clvmd.service lvm2-cluster-activation.service

%preun cluster-standalone
%systemd_preun lvm2-clvmd.service lvm2-cluster-activation.service

%postun cluster-standalone
%systemd_postun lvm2-clvmd.service lvm2-cluster-activation.service

%files cluster-standalone
%defattr(555,root,root,-)
%{_prefix}/lib/systemd/lvm2-cluster-activation
%defattr(444,root,root,-)
%{_unitdir}/lvm2-clvmd.service
%{_unitdir}/lvm2-cluster-activation.service

%endif

###############################################################################
# Cluster mirror subpackage
# The 'clvm' OCF script to manage cmirrord instance is part of resource-agents.
###############################################################################
%if %{enable_cluster}
%if %{enable_cmirror}

%package -n cmirror
Summary: Daemon for device-mapper-based clustered mirrors
Group: System Environment/Base
Requires: corosync >= %{corosync_version}
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: resource-agents >= %{resource_agents_version}

%description -n cmirror
Daemon providing device-mapper-based mirrors in a shared-storage cluster.

%files -n cmirror
%defattr(555,root,root,-)
%{_sbindir}/cmirrord
%attr(444, -, -) %{_mandir}/man8/cmirrord.8.gz

##############################################################################
# Cmirror-standalone subpackage
##############################################################################
%package -n cmirror-standalone
Summary: Additional files to support device-mapper-based clustered mirrors in standalone mode
License: GPLv2
Group: System Environment/Base
Requires: cmirror >= %{epoch}:%{version}-%{release}

%description -n cmirror-standalone

Additional files needed to run daemon for device-mapper-based clustered
mirrors in standalone mode as a service without cluster resource manager
involvement (e.g. pacemaker).

%post -n cmirror-standalone
%systemd_post lvm2-cmirrord.service

%preun -n cmirror-standalone
%systemd_preun lvm2-cmirrord.service

%postun -n cmirror-standalone
%systemd_postun lvm2-cmirrord.service

%files -n cmirror-standalone
%defattr(444,root,root,-)
%{_unitdir}/lvm2-cmirrord.service

%endif
%endif

##############################################################################
# Device-mapper subpackages
##############################################################################
%package -n device-mapper
Summary: Device mapper utility
Version: %{device_mapper_version}
License: GPLv2
Group: System Environment/Base
URL: http://sources.redhat.com/dm
Requires: device-mapper-libs = %{device_mapper_version}-%{release}
Requires: util-linux >= %{util_linux_version}
Requires: systemd >= %{systemd_version}
# We need dracut to install required udev rules if udev_sync
# feature is turned on so we don't lose required notifications.
Conflicts: dracut < %{dracut_version}

%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%files -n device-mapper
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%doc WHATS_NEW_DM VERSION_DM README
%doc udev/12-dm-permissions.rules
%defattr(444,root,root,-)
%attr(555, -, -) %{_sbindir}/dmsetup
%{_mandir}/man8/dmsetup.8.gz
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%package -n device-mapper-devel
Summary: Development libraries and headers for device-mapper
Version: %{device_mapper_version}
License: LGPLv2
Group: Development/Libraries
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%files -n device-mapper-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%package -n device-mapper-libs
Summary: Device-mapper shared library
Version: %{device_mapper_version}
License: LGPLv2
Group: System Environment/Libraries
Requires: device-mapper = %{device_mapper_version}-%{release}

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%post -n device-mapper-libs -p /sbin/ldconfig

%postun -n device-mapper-libs -p /sbin/ldconfig

%files -n device-mapper-libs
%defattr(555,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%{_libdir}/libdevmapper.so.*

%package -n device-mapper-event
Summary: Device-mapper event daemon
Group: System Environment/Base
Version: %{device_mapper_version}
Requires: device-mapper = %{device_mapper_version}-%{release}
Requires: device-mapper-event-libs = %{device_mapper_version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.socket
if [ -e %{_default_pid_dir}/dmeventd.pid ]; then
	%{_sbindir}/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."
fi

%preun -n device-mapper-event
%systemd_preun dm-event.service dm-event.socket

%files -n device-mapper-event
%defattr(444,root,root,-)
%attr(555, -, -) %{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%package -n device-mapper-event-libs
Summary: Device-mapper event daemon shared library
Version: %{device_mapper_version}
License: LGPLv2
Group: System Environment/Libraries

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%post -n device-mapper-event-libs -p /sbin/ldconfig

%postun -n device-mapper-event-libs -p /sbin/ldconfig

%files -n device-mapper-event-libs
%defattr(555,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%{_libdir}/libdevmapper-event.so.*

%package -n device-mapper-event-devel
Summary: Development libraries and headers for the device-mapper event daemon
Version: %{device_mapper_version}
License: LGPLv2
Group: Development/Libraries
Requires: device-mapper-event = %{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%files -n device-mapper-event-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

%changelog
