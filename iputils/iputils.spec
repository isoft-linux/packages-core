Summary: Network monitoring tools including ping
Name: iputils
Version: 20121221
Release: 1 
License: BSD and GPLv2+
URL: http://www.skbuff.net/iputils
Group: Core/Runtime/Utility

Source0: http://www.skbuff.net/iputils/%{name}-s%{version}.tar.bz2

BuildRequires: openssl-devel
BuildRequires: libcap-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires: filesystem >= 3
Provides: /bin/ping
Provides: /bin/ping6
Provides: /sbin/arping
Provides: /sbin/rdisc

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%prep
%setup -q -n %{name}-s%{version}

%build
make USE_GNUTLS=no KERNEL_INCLUDE=/usr/include

%install
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
for i in arping clockdiff ipg rarpd rdisc tftpd tracepath tracepath6; do
    install -D -m755 $i $RPM_BUILD_ROOT/usr/sbin/$i
done
for i in ping ping6 traceroute6; do
    install -D -m4755 $i $RPM_BUILD_ROOT/usr/bin/$i
done

%files
%attr(0755,root,root) %caps(cap_net_raw=ep) %{_sbindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=ep) %{_sbindir}/arping
%attr(0755,root,root) %caps(cap_net_raw=ep cap_net_admin=ep) %{_bindir}/ping
%{_sbindir}/rdisc
%attr(0755,root,root) %caps(cap_net_raw=ep cap_net_admin=ep) %{_bindir}/ping6
%{_sbindir}/ipg
%{_sbindir}/rarpd
%{_sbindir}/tftpd

%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%{_bindir}/ping6
%{_bindir}/traceroute6
#%attr(644,root,root) %{_mandir}/man8/clockdiff.8.gz
#%attr(644,root,root) %{_mandir}/man8/arping.8.gz
#%attr(644,root,root) %{_mandir}/man8/ping.8.gz
#%attr(644,root,root) %{_mandir}/man8/ping6.8.gz
#%attr(644,root,root) %{_mandir}/man8/rdisc.8.gz
#%attr(644,root,root) %{_mandir}/man8/tracepath.8.gz
#%attr(644,root,root) %{_mandir}/man8/tracepath6.8.gz
#%attr(644,root,root) %{_mandir}/man8/ifenslave.8.gz

