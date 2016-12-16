%global libnfnetlink_ver 1.0.1
%define script_path %{_libexecdir}/iptables

# service legacy actions (RHBZ#748134)
%define legacy_actions %{_libexecdir}/initscripts/legacy-actions

Name: iptables
Summary: Tools for managing Linux kernel packet filtering capabilities
Version: 1.6.0
Release: 1
Source:  http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1: iptables.init
Source2: iptables-config
Source3: iptables.service
Source4: iptables.save-legacy


Source10: libnfnetlink-%{libnfnetlink_ver}.tar.bz2
Patch10: libnfnetlink-musl-fix.patch

URL: http://www.netfilter.org/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: GPLv2
BuildRequires: kernel-headers
Conflicts: kernel < 2.4.20
BuildRequires: systemd-units
BuildRequires: bison flex libnftnl-devel libmnl-devel

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%package devel
Summary: Development package for iptables
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
iptables development headers and libraries.

The iptc interface is upstream marked as not public. The interface is not 
stable and may change with every new version. It is therefore unsupported.

%package services
Summary: iptables and ip6tables services for iptables
Requires: %{name} = %{version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: systemd < 38
Conflicts: filesystem < 3
# provide and obsolete old main package
Provides: %{name} = 1.4.16.1
Obsoletes: %{name} <= 1.4.16.1
# provide and obsolte ipv6 sub package
Provides: %{name}-ipv6 = 1.4.11.1
Obsoletes: %{name}-ipv6 <= 1.4.11.1

%description services
iptables services for IPv4 and IPv6

This package provides the services iptables and ip6tables that have been split
out of the base package since they are not active by default anymore.

%package utils
Summary: iptables and ip6tables services for iptables
Requires: %{name} = %{version}-%{release}

%description utils
Utils for iptables.

Currently only provides nfnl_osf with the pf.os database.


%prep
%setup -q -a10
sed -i -e '/if_packet/i#define __aligned_u64 __u64 __attribute__((aligned(8)))' \
        extensions/libxt_pkttype.c
%build
pushd libnfnetlink-%{libnfnetlink_ver}
cat %{PATCH10} |patch -p1
CFLAGS="-fPIC" ./configure --prefix=`pwd`/../interbin --disable-shared --enable-static
make %{?_smp_mflags}
make install
popd

export PKG_CONFIG_PATH=`pwd`/interbin/lib/pkgconfig

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
%configure \
        --without-kernel \
        --enable-devel \
        --enable-shared \

# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} 
# remove la file(s)
rm -f %{buildroot}/%{_libdir}/*.la

# install ip*tables.h header files
install -m 644 include/ip*tables.h %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_includedir}/iptables
install -m 644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables/

# install ipulog header file
install -d -m 755 %{buildroot}%{_includedir}/libipulog/
install -m 644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

# install init scripts and configuration files
install -d -m 755 %{buildroot}%{script_path}
install -c -m 755 %{SOURCE1} %{buildroot}%{script_path}/iptables.init
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables.init
install -c -m 755 ip6tables.init %{buildroot}%{script_path}/ip6tables.init
install -d -m 755 %{buildroot}/etc/sysconfig
install -c -m 755 %{SOURCE2} %{buildroot}/etc/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE2} > ip6tables-config
install -c -m 755 ip6tables-config %{buildroot}/etc/sysconfig/ip6tables-config

# install systemd service files
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}
sed -e 's;iptables;ip6tables;g' -e 's;IPv4;IPv6;g' -e 's;/usr/libexec/ip6tables;/usr/libexec/iptables;g' < %{SOURCE3} > ip6tables.service
install -c -m 644 ip6tables.service %{buildroot}/%{_unitdir}

# install legacy actions for service command
install -d %{buildroot}/%{legacy_actions}/iptables
install -d %{buildroot}/%{legacy_actions}/ip6tables
install -c -m 755 %{SOURCE4} %{buildroot}/%{legacy_actions}/iptables/save
sed -e 's;iptables.init;ip6tables.init;g' -e 's;IPTABLES;IP6TABLES;g' < %{buildroot}/%{legacy_actions}/iptables/save > ip6tabes.save-legacy
install -c -m 755 ip6tabes.save-legacy %{buildroot}/%{legacy_actions}/ip6tables/save

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post services
if [ $1 -eq 1 ] ; then # Initial installation
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%if %{with default_service}
   /bin/systemctl enable iptables.service >/dev/null 2>&1 || :
   /bin/systemctl enable ip6tables.service >/dev/null 2>&1 || :
%endif
fi

%preun services
if [ $1 -eq 0 ]; then # Package removal, not upgrade
   /bin/systemctl --no-reload disable iptables.service > /dev/null 2>&1 || :
   /bin/systemctl --no-reload disable ip6tables.service > /dev/null 2>&1 || :
   /bin/systemctl stop iptables.service > /dev/null 2>&1 || :
   /bin/systemctl stop ip6tables.service > /dev/null 2>&1 || :
fi

%postun services
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then # Package upgrade, not uninstall
   /bin/systemctl try-restart iptables.service >/dev/null 2>&1 || :
   /bin/systemctl try-restart ip6tables.service >/dev/null 2>&1 || :
fi

# Autostart
%if %{with default_service}
/bin/systemctl --no-reload enable iptables.service >/dev/null 2>&1 ||:
%endif

%if %{with default_service}
/bin/systemctl --no-reload enable ip6tables.service >/dev/null 2>&1 ||:
%endif


%files
%defattr(-,root,root)
%doc COPYING INSTALL INCOMPATIBILITIES
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/iptables-config
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/ip6tables-config
%{_sbindir}/iptables*
%{_sbindir}/ip6tables*
%{_sbindir}/xtables-multi
%{_sbindir}/arptables-compat
%{_sbindir}/ebtables-compat
%{_sbindir}/xtables-compat-multi
%{_bindir}/iptables-xml
%{_mandir}/man1/iptables-xml*
%{_mandir}/man8/iptables*
%{_mandir}/man8/ip6tables*
%dir %{_libdir}/xtables
%{_libdir}/xtables/libipt*
%{_libdir}/xtables/libip6t*
%{_libdir}/xtables/libxt*
%{_libdir}/libip*tc.so.*
%{_libdir}/libxtables.so.*
/etc/ethertypes
%{_libdir}/xtables/libarpt*
%{_libdir}/xtables/libebt*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/iptables
%{_includedir}/iptables/*.h
%{_includedir}/*.h
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libipulog
%{_includedir}/libipulog/*.h
%{_libdir}/libip*tc.so
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/libiptc.pc
%{_libdir}/pkgconfig/libip4tc.pc
%{_libdir}/pkgconfig/libip6tc.pc
%{_libdir}/pkgconfig/xtables.pc

%files services
%attr(0755,root,root) %{script_path}/iptables.init
%attr(0755,root,root) %{script_path}/ip6tables.init
%dir %{script_path}
%{_unitdir}/iptables.service
%{_unitdir}/ip6tables.service
%dir %{legacy_actions}/iptables
%{legacy_actions}/iptables/save
%dir %{legacy_actions}/ip6tables
%{legacy_actions}/ip6tables/save

%files utils
%{_sbindir}/nfnl_osf
%dir %{_datadir}/xtables
%{_datadir}/xtables/pf.os

%changelog
* Fri Dec 16 2016 sulit - 1.6.0-1
- upgrade iptables to 1.6.0

* Fri Oct 23 2015 cjacker - 1.4.21-2
- Rebuild for new 4.0 release

