#
# Copyright (C)  Heinz Mauelshagen, 2004-2010 Red Hat GmbH. All rights reserved.
#
# See file LICENSE at the top of this source tree for license information.
#

Summary: dmraid (Device-mapper RAID tool and library)
Name: dmraid
Version: 1.0.0.rc16
Release: 25%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://people.redhat.com/heinzm/sw/dmraid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: device-mapper-devel >= 1.02.02-2
BuildRequires: device-mapper-event-devel
BuildRequires: systemd
Requires: device-mapper >= 1.02.02-2
Requires: dmraid-events
Requires: kpartx
Requires: systemd
Requires(post): systemd >= 195-4
Obsoletes: dmraid-libs < %{version}-%{release}
Provides: dmraid-libs = %{version}-%{release}
Source0: ftp://people.redhat.com/heinzm/sw/dmraid/src/%{name}-%{version}.tar.bz2
Source1: fedora-dmraid-activation
Source2: dmraid-activation.service

Patch0: dmraid-1.0.0.rc16-test_devices.patch
Patch1: ddf1_lsi_persistent_name.patch
Patch2: pdc_raid10_failure.patch
Patch3: return_error_wo_disks.patch
Patch4: fix_sil_jbod.patch
Patch5: avoid_register.patch
Patch6: move_pattern_file_to_var.patch
Patch7: libversion.patch
Patch8: libversion-display.patch

Patch9: bz635995-data_corruption_during_activation_volume_marked_for_rebuild.patch
# Patch10: bz626417_8-faulty_message_after_unsuccessful_vol_registration.patch
Patch11: bz626417_19-enabling_registration_degraded_volume.patch
Patch12: bz626417_20-cleanup_some_compilation_warning.patch
Patch13: bz626417_21-add_option_that_postpones_any_metadata_updates.patch

%description
DMRAID supports RAID device discovery, RAID set activation, creation,
removal, rebuild and display of properties for ATARAID/DDF1 metadata on
Linux >= 2.4 using device-mapper.

%package -n dmraid-devel
Summary: Development libraries and headers for dmraid.
Group: Development/Libraries
Requires: dmraid = %{version}-%{release}, sgpio

%description -n dmraid-devel
dmraid-devel provides a library interface for RAID device discovery,
RAID set activation and display of properties for ATARAID volumes.

%package -n dmraid-events
Summary: dmevent_tool (Device-mapper event tool) and DSO
Group: System Environment/Base
Requires: dmraid = %{version}-%{release}, sgpio
Requires: device-mapper-event

%description -n dmraid-events
Provides a dmeventd DSO and the dmevent_tool to register devices with it
for device monitoring.  All active RAID sets should be manually registered
with dmevent_tool.

#%package -n dmraid-events-logwatch
#Summary: dmraid logwatch-based email reporting
#Group: System Environment/Base
#Requires: dmraid-events = %{version}-%{release}, logwatch
#Requires: crontabs
#
#%description -n dmraid-events-logwatch
#Provides device failure reporting via logwatch-based email reporting.
#Device failure reporting has to be activated manually by activating the 
#/etc/cron.d/dmeventd-logwatch entry and by calling the dmevent_tool
#(see manual page for examples) for any active RAID sets.

%prep
%setup -q -n dmraid/%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%patch9 -p1
# %patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
%define _libdir /%{_lib}

%configure --prefix=${RPM_BUILD_ROOT}/usr --sbindir=${RPM_BUILD_ROOT}/sbin --libdir=${RPM_BUILD_ROOT}/%{_libdir} --mandir=${RPM_BUILD_ROOT}/%{_mandir} --includedir=${RPM_BUILD_ROOT}/%{_includedir} --enable-debug --disable-libselinux --disable-libsepol --disable-static_link --enable-led --enable-intel_led
# make DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT{%{_libdir},/sbin,%{_sbindir},%{_bindir},%{_libdir},%{_includedir}/dmraid/,/var/lock/dmraid,/etc/cron.d/,/etc/logwatch/conf/services/,/etc/logwatch/scripts/services/,/var/cache/logwatch/dmeventd}
make DESTDIR=$RPM_BUILD_ROOT install
ln -s dmraid $RPM_BUILD_ROOT/sbin/dmraid.static

# Provide convenience link from dmevent_tool
(cd $RPM_BUILD_ROOT/sbin ; ln -f dmevent_tool dm_dso_reg_tool)
(cd $RPM_BUILD_ROOT/%{_mandir}/man8 ; ln -f dmevent_tool.8 dm_dso_reg_tool.8 ; ln -f dmraid.8 dmraid.static.8)

install -m 644 include/dmraid/*.h $RPM_BUILD_ROOT%{_includedir}/dmraid/

# Install the libdmraid and libdmraid-events (for dmeventd) DSO
# Create version symlink to libdmraid.so.1 we link against
install -m 755 lib/libdmraid.so $RPM_BUILD_ROOT%{_libdir}/libdmraid.so.%{version}
(cd $RPM_BUILD_ROOT/%{_libdir} ; ln -sf libdmraid.so.%{version} libdmraid.so ; ln -sf libdmraid.so.%{version} libdmraid.so.1)
install -m 755 lib/libdmraid-events-isw.so $RPM_BUILD_ROOT%{_libdir}/libdmraid-events-isw.so.%{version}
(cd $RPM_BUILD_ROOT/%{_libdir} ; ln -sf libdmraid-events-isw.so.%{version} libdmraid-events-isw.so ; ln -sf libdmraid-events-isw.so.%{version} libdmraid-events-isw.so.1)

# Install logwatch config file and script for dmeventd
install -m 644 logwatch/dmeventd.conf $RPM_BUILD_ROOT/etc/logwatch/conf/services/dmeventd.conf
install -m 755 logwatch/dmeventd $RPM_BUILD_ROOT/etc/logwatch/scripts/services/dmeventd
install -m 644 logwatch/dmeventd_cronjob.txt $RPM_BUILD_ROOT/etc/cron.d/dmeventd-logwatch
install -m 0700 /dev/null $RPM_BUILD_ROOT/var/cache/logwatch/dmeventd/syslogpattern.txt

# Install systemd unit
install -d ${RPM_BUILD_ROOT}/%{_prefix}/lib/systemd
install -d ${RPM_BUILD_ROOT}/%{_unitdir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/fedora-dmraid-activation
install -m 444 %{SOURCE2} $RPM_BUILD_ROOT/%{_unitdir}/dmraid-activation.service

rm -f $RPM_BUILD_ROOT/%{_libdir}/libdmraid.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post dmraid-activation.service

%postun
/sbin/ldconfig

# 1. Main package
%files
%defattr(-,root,root)
%doc CHANGELOG CREDITS KNOWN_BUGS LICENSE LICENSE_GPL LICENSE_LGPL README TODO doc/dmraid_design.txt
/%{_mandir}/man8/dmraid*
/sbin/dmraid
/sbin/dmraid.static
%{_libdir}/libdmraid.so*
%{_libdir}/libdmraid-events-isw.so*
%{_prefix}/lib/systemd/fedora-dmraid-activation
%{_unitdir}/dmraid-activation.service
%ghost /var/lock/dmraid

# 2. Development package
%files -n dmraid-devel
%defattr(-,root,root)
%dir %{_includedir}/dmraid
%{_includedir}/dmraid/*

# 3. Event (device montoring) package
%files -n dmraid-events
%defattr(-,root,root)
/%{_mandir}/man8/dmevent_tool*
/%{_mandir}/man8/dm_dso_reg_tool*
/sbin/dmevent_tool
/sbin/dm_dso_reg_tool

# 4. Event package to support logwatch monitoring
#%files -n dmraid-events-logwatch
#%defattr(-,root,root)
#%config(noreplace) /etc/logwatch/*
#%config(noreplace) /etc/cron.d/dmeventd-logwatch
#%dir /var/cache/logwatch/dmeventd
#%ghost /var/cache/logwatch/dmeventd/syslogpattern.txt

%changelog
