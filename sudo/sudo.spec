Summary: Allows restricted root access for specified users
Name: sudo
Version: 1.8.15
Release: 3
License: ISC
URL: http://www.courtesan.com/sudo/
Source0: http://www.courtesan.com/sudo/dist/sudo-%{version}.tar.gz

#NOTE: HOME also will be keeped. this will fix "sudo" can not get correct theme of gtk/qt 
Source1: sudo-1.8.8-sudoers 


# don't strip
Patch1: sudo-1.6.7p5-strip.patch
# Patch to read ldap.conf more closely to nss_ldap
Patch2: sudo-1.8.14p1-ldapconfpatch.patch
# Patch makes changes in documentation bz:1162070
Patch3: sudo-1.8.14p1-docpassexpire.patch
# Patch initialize variable before executing sudo_strsplit
Patch4: sudo-1.8.14p3-initialization.patch


Requires: /etc/pam.d/system-auth, vim
Requires(post): /bin/chmod

BuildRequires: pam-devel
BuildRequires: groff
BuildRequires: flex
BuildRequires: bison
BuildRequires: automake autoconf libtool
BuildRequires: audit-libs-devel libcap-devel
BuildRequires: gettext
BuildRequires: zlib-devel
#for systemd rpm macros
BuildRequires: systemd-devel
%description
Sudo (superuser do) allows a system administrator to give certain
users (or groups of users) the ability to run some (or all) commands
as root while logging all commands and arguments. Sudo operates on a
per-command basis.  It is not a replacement for the shell.  Features
include: the ability to restrict what commands a user may run on a
per-host basis, copious logging of each command (providing a clear
audit trail of who did what), a configurable timeout of the sudo
command, and the ability to use the same configuration file (sudoers)
on many different machines.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files developing sudo
plugins that use %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .strip
%patch2 -p1 -b .ldapconfpatch
%patch3 -p1 -b .docpassexpire
%patch4 -p1 -b .initialization

%build
autoreconf -I m4 -fv --install

%ifarch s390 s390x sparc64
F_PIE=-fPIE
%else
F_PIE=-fpie
%endif

export CFLAGS="$RPM_OPT_FLAGS $F_PIE" LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"

%configure \
        --prefix=%{_prefix} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --with-logging=syslog \
        --with-logfac=authpriv \
        --with-pam \
        --with-pam-login \
        --with-editor=/bin/vi \
        --with-env-editor \
        --with-ignore-dot \
        --with-tty-tickets \
        --without-ldap \
        --without-selinux \
        --with-passprompt="[sudo] password for %p: " \
        --with-linux-audit \
        --with-sssd
#       --without-kerb5 \
#       --without-kerb4
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

chmod 755 $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_sbindir}/* 
install -p -d -m 700 $RPM_BUILD_ROOT/var/db/sudo
install -p -d -m 750 $RPM_BUILD_ROOT/etc/sudoers.d
install -p -c -m 0440 %{SOURCE1} $RPM_BUILD_ROOT/etc/sudoers

chmod +x $RPM_BUILD_ROOT%{_libexecdir}/sudo/*.so # for stripping, reset in %%files

%find_lang sudo
%find_lang sudoers

cat sudo.lang sudoers.lang > sudo_all.lang
rm sudo.lang sudoers.lang

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
cat > $RPM_BUILD_ROOT/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-auth
password   include      system-auth
session    optional     pam_keyinit.so revoke
session    required     pam_limits.so
session    include      system-auth
EOF


cat > $RPM_BUILD_ROOT/etc/pam.d/sudo-i << EOF
#%%PAM-1.0
auth       include      sudo
account    include      sudo
password   include      sudo
session    optional     pam_keyinit.so force revoke
session    include      sudo
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files -f sudo_all.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) /etc/sudoers
%attr(0750,root,root) %dir /etc/sudoers.d/
%config(noreplace) /etc/pam.d/sudo
%config(noreplace) /etc/pam.d/sudo-i
%attr(0644,root,root) %{_tmpfilesdir}/sudo.conf
%dir /var/db/sudo
%attr(4111,root,root) %{_bindir}/sudo
%attr(4111,root,root) %{_bindir}/sudoedit
%attr(0111,root,root) %{_bindir}/sudoreplay
%attr(0755,root,root) %{_sbindir}/visudo
%dir %{_libexecdir}/sudo
%attr(0644,root,root) %{_libexecdir}/sudo/sudo_noexec.so
%attr(0644,root,root) %{_libexecdir}/sudo/sudoers.so
%attr(0644,root,root) %{_libexecdir}/sudo/group_file.so
%attr(0644,root,root) %{_libexecdir}/sudo/system_group.so
%attr(0644,root,root) %{_libexecdir}/sudo/libsudo_util.so.?.?.?
%{_libexecdir}/sudo/libsudo_util.so.?
%{_mandir}/man5/sudoers.5*
%{_mandir}/man5/sudo.conf.5*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%{_docdir}/*

# Make sure permissions are ok even if we're updating
%post
/bin/chmod 0440 /etc/sudoers || :

%files devel
%defattr(-,root,root,-)
%doc plugins/sample/sample_plugin.c
%{_includedir}/sudo_plugin.h
%{_mandir}/man8/sudo_plugin.8*
%{_libexecdir}/sudo/libsudo_util.so

%changelog
* Wed Nov 25 2015 xiaotian.wu@i-soft.com.cn - 1.8.15-3
- %wheel groups use nopassword.

* Fri Oct 23 2015 cjacker - 1.8.10-2
- Rebuild for new 4.0 release

* Sat Dec 21 2013 Cjacker <cjacker@gmail.com>
- update to 1.8.8
