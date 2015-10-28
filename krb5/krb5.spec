#NOTE:!!!!!!!!!!!!!!!!!!!!!!!!!
#we only build krb5 client libraries and utilities for DESKTOP!!!!!!!!!!!!!!

%global WITH_OPENSSL 1

%global gettext_domain mit-krb5

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.13.2
Release: 2
Source0: krb5-1.13.2.tar.gz
 
Source2: krb5.conf
Source29:ksu.pamd

License: MIT
URL: http://web.mit.edu/kerberos/www/
BuildRequires: autoconf, bison, flex, gawk, gettext
BuildRequires: libcom_err-devel, libss-devel
BuildRequires: gzip, ncurses-devel, tar
BuildRequires: pam-devel
BuildRequires: systemd-units
BuildRequires: net-tools
BuildRequires: libverto-devel

BuildRequires: openssl-devel >= 0.9.8

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of sending passwords over the network in unencrypted form.

%package devel
Summary: Development files needed to compile Kerberos 5 programs
Requires: %{name}-libs = %{version}-%{release}
Requires: libcom_err-devel

%description devel
Kerberos is a network authentication system. The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you need
to install this package.

%package libs
Summary: The shared libraries used by Kerberos 5

%description libs
Kerberos is a network authentication system. The krb5-libs package
contains the shared libraries needed by Kerberos 5. If you are using
Kerberos, you need to install this package.

%package workstation
Summary: Kerberos 5 programs for use on workstations
Requires: %{name}-libs = %{version}-%{release}
# mktemp is used by krb5-send-pr
Requires: coreutils

%description workstation
Kerberos is a network authentication system. The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be
installed on every workstation.

%package pkinit
Summary: The PKINIT module for Kerberos 5
Requires: %{name}-libs = %{version}-%{release}

%description pkinit
Kerberos is a network authentication system. The krb5-pkinit
package contains the PKINIT plugin, which allows clients
to obtain initial credentials from a KDC using a private key and a
certificate.

%prep
%setup -q -n %{name}-%{version} 
ln -s NOTICE LICENSE

%build
pushd src
# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all`"
CPPFLAGS="`echo $DEFINES $INCLUDES`"

%configure \
	CC="cc" \
	CFLAGS="$CFLAGS" \
	CPPFLAGS="$CPPFLAGS" \
	SS_LIB="-lss" \
	--enable-shared \
    --disable-nls \
	--localstatedir=%{_var}/kerberos \
	--disable-rpath \
	--with-system-et \
	--with-system-ss \
	--with-netlib=-lresolv \
	--without-tcl \
	--enable-dns-for-realm \
	--without-ldap \
	--enable-pkinit \
    --with-dirsrv-account-locking \
    --with-pkinit-crypto-impl=openssl \
    --with-tls-impl=openssl \
	--with-system-verto \
	--with-pam \
	--without-selinux


make %{?_smp_mflags}
popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/krb5.conf

# Where per-user keytabs live by default.
mkdir -p $RPM_BUILD_ROOT%{_var}/kerberos/krb5/user

# PAM configuration files.
mkdir -p $RPM_BUILD_ROOT/etc/pam.d/
for pam in \
    %{SOURCE29} ; do
    install -pm 644 ${pam} \
    $RPM_BUILD_ROOT/etc/pam.d/`basename ${pam} .pamd`
done

# Plug-in directories.
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/preauth
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/kdb
install -pdm 755 $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/authdata


# The rest of the binaries, headers, libraries, and docs.
make -C src DESTDIR=$RPM_BUILD_ROOT EXAMPLEDIR=%{_docdir}/krb5-libs-%{version}/examples install

# Munge krb5-config yet again.  This is totally wrong for 64-bit, but chunks
# of the buildconf patch already conspire to strip out /usr/<anything> from the
# list of link flags, and it helps prevent file conflicts on multilib systems.
sed -r -i -e 's|^libdir=/usr/lib(64)?$|libdir=/usr/lib|g' $RPM_BUILD_ROOT%{_bindir}/krb5-config

chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so*


#drop server related files.
rm -rf %{buildroot}%{_sbindir}/kadmin.local
rm -rf %{buildroot}%{_sbindir}/kadmind
rm -rf %{buildroot}%{_sbindir}/kdb5_ldap_util
rm -rf %{buildroot}%{_sbindir}/kdb5_util
rm -rf %{buildroot}%{_sbindir}/kprop
rm -rf %{buildroot}%{_sbindir}/kpropd
rm -rf %{buildroot}%{_sbindir}/kproplog
rm -rf %{buildroot}%{_sbindir}/krb5kdc

rm -rf %{buildroot}%{_mandir}/man1/k5srvutil.1*
rm -rf %{buildroot}%{_mandir}/man5/kadm5.acl.5*
rm -rf %{buildroot}%{_mandir}/man5/kdc.conf.5*
rm -rf %{buildroot}%{_mandir}/man8/kadmin.local.8*
rm -rf %{buildroot}%{_mandir}/man8/kadmind.8*
rm -rf %{buildroot}%{_mandir}/man8/kdb5_ldap_util.8*
rm -rf %{buildroot}%{_mandir}/man8/kdb5_util.8*
rm -rf %{buildroot}%{_mandir}/man8/kprop.8*
rm -rf %{buildroot}%{_mandir}/man8/kpropd.8*
rm -rf %{buildroot}%{_mandir}/man8/kproplog.8*
rm -rf %{buildroot}%{_mandir}/man8/krb5kdc.8*


%find_lang %{gettext_domain}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files workstation
%defattr(-,root,root,-)
# Clients of the KDC, including tools you're likely to need if you're running
# app servers other than those built from this source package.
%{_bindir}/kdestroy
%{_bindir}/kinit
%{_bindir}/klist
%{_bindir}/kpasswd
%{_bindir}/kswitch
%{_bindir}/kvno
%{_bindir}/kadmin
%{_bindir}/k5srvutil
%{_bindir}/ktutil
   
# Doesn't really fit anywhere else.
%attr(4755,root,root) %{_bindir}/ksu
%config(noreplace) /etc/pam.d/ksu

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr

%{_mandir}/man1/kinit.1.gz
%{_mandir}/man1/kdestroy.1.gz
%{_mandir}/man1/klist.1.gz
%{_mandir}/man1/kpasswd.1.gz
%{_mandir}/man1/kvno.1.gz
%{_mandir}/man1/kswitch.1.gz
%{_mandir}/man1/kadmin.1.gz
%{_mandir}/man1/ktutil.1.gz
%{_mandir}/man1/ksu.1*

%files libs -f %{gettext_domain}.lang 
%defattr(-,root,root,-)
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/krb5.conf
%{_libdir}/libgssapi_krb5.so.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
%{_libdir}/libkrad.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%{_libdir}/krb5/plugins/kdb/db2.so
%{_libdir}/krb5/plugins/preauth/otp.so
%{_libdir}/krb5/plugins/tls/k5tls.so
%dir %{_var}/kerberos
%dir %{_var}/kerberos/krb5
%dir %{_var}/kerberos/krb5/user
   
%{_mandir}/man5/.k5identity.5.gz
%{_mandir}/man5/.k5login.5.gz
%{_mandir}/man5/k5identity.5.gz
%{_mandir}/man5/k5login.5.gz
%{_mandir}/man5/krb5.conf.5.gz

%files pkinit
%defattr(-,root,root,-)
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrad.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so

%{_bindir}/krb5-config
%{_bindir}/sclient
%{_sbindir}/sserver
%{_mandir}/man1/krb5-config.1.gz
%{_mandir}/man1/sclient.1.gz
%{_mandir}/man8/sserver.8.gz

# Protocol test clients.
%{_bindir}/sim_client
%{_bindir}/gss-client
%{_bindir}/uuclient

# Protocol test servers.
%{_sbindir}/sim_server
%{_sbindir}/gss-server
%{_sbindir}/uuserver
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.13.2-2
- Rebuild for new 4.0 release

