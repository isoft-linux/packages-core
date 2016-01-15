# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Build position-independent executables (requires toolchain support)?
%define pie 1

# Do we want libedit support
%define libedit 1

# Do not forget to bump pam_ssh_agent_auth release if you rewind the main package release to 1
%define openssh_ver 7.1p2
%define openssh_rel 1 

Summary: An open source implementation of SSH protocol versions 1 and 2
Name: openssh
Version: %{openssh_ver}
Release: %{openssh_rel}.1
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source2: sshd.pam
Source7: sshd.sysconfig
Source9: sshd@.service
Source10: sshd.socket
Source11: sshd.service
Source12: sshd-keygen.service
Source13: sshd-keygen

Patch0: openssh-7.1p1-hostkeyalgorithms.patch

License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: /sbin/nologin

BuildRequires: autoconf, automake, perl, zlib-devel
BuildRequires: util-linux, groff
BuildRequires: pam-devel
BuildRequires: openssl-devel

BuildRequires: libedit-devel ncurses-devel
BuildRequires: systemd

%package clients
Summary: An open source SSH client applications
Requires: openssh = %{version}-%{release}

%package server
Summary: An open source SSH server daemon
Requires: openssh = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%prep
%setup -q 
%patch0 -p1

%build
# the -fvisibility=hidden is needed for clean build of the pam_ssh_agent_auth
# and it makes the ssh build more clean and even optimized better
CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"; export CFLAGS

CFLAGS="$CFLAGS -fpic"

SAVE_LDFLAGS="$LDFLAGS"

LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--without-tcp-wrappers \
	--with-default-path=/usr/local/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--enable-vendor-patchlevel="Elsa-%{version}-%{release}" \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--disable-lastlog \
    	--disable-wtmp \
    	--without-tcp-wrappers \
	--with-pam \
	--without-kerberos5 \
	--with-libedit \
	--with-ssh1

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ldap.conf

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m755 %{SOURCE13} $RPM_BUILD_ROOT/%{_sbindir}/sshd-keygen
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.service
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :

%pre server
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :

%post server
%systemd_post sshd.service sshd.socket

%preun server
%systemd_preun sshd.service sshd.socket

%postun server
%systemd_postun_with_restart sshd.service

%files
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(2111,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %{_bindir}/slogin
%attr(0644,root,root) %{_mandir}/man1/slogin.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%attr(2111,root,nobody) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*

%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_sbindir}/sshd-keygen
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd
%attr(0644,root,root) %{_unitdir}/sshd.service
%attr(0644,root,root) %{_unitdir}/sshd@.service
%attr(0644,root,root) %{_unitdir}/sshd.socket
%attr(0644,root,root) %{_unitdir}/sshd-keygen.service



%changelog
* Fri Jan 15 2016 xiaotian.wu@i-soft.com.cn - 7.1p2-1.1
- new version.
- fixed client bugs CVE-2016-0777 and CVE-2016-0778

* Fri Oct 23 2015 cjacker - 7.1p1-4.1
- Rebuild for new 4.0 release

* Mon Aug 24 2015 Cjacker <cjacker@foxmail.com>
- add patch from http://lists.mindrot.org/pipermail/openssh-unix-dev/2015-August/034324.html
- enable --with-ssh1 to fix keygen issue.
- 
* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 7.0

* Thu Jul 23 2015 Cjacker <cjacker@foxmail.com>
- Patch6 for CVE-2015-5600: only query each keyboard-interactive device once

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

