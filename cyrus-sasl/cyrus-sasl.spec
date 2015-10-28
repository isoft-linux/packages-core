%define username    saslauth
%define hint        Saslauthd user
%define homedir     /run/saslauthd

%define _plugindir2 %{_libdir}/sasl2
%define bootstrap_cyrus_sasl 1 

Summary: The Cyrus SASL library
Name: cyrus-sasl
Version: 2.1.26
Release: 25
License: BSD with advertising
# Source0 originally comes from ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/;
# make-no-dlcompatorsrp-tarball.sh removes the "dlcompat" subdirectory and builds a
# new tarball.
Source0: cyrus-sasl-%{version}-nodlcompatorsrp.tar.gz
Source5: saslauthd.service
Source7: sasl-mechlist.c
Source8: sasl-checkpass.c
Source9: saslauthd.sysconfig
Source10: make-no-dlcompatorsrp-tarball.sh
Source11: saslauthd.tmpfiles
URL: http://asg.web.cmu.edu/sasl/sasl-library.html
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Patch11: cyrus-sasl-2.1.25-no_rpath.patch
Patch15: cyrus-sasl-2.1.20-saslauthd.conf-path.patch
Patch23: cyrus-sasl-2.1.23-man.patch
Patch24: cyrus-sasl-2.1.21-sizes.patch
Patch31: cyrus-sasl-2.1.22-kerberos4.patch
Patch32: cyrus-sasl-2.1.26-warnings.patch
Patch34: cyrus-sasl-2.1.22-ldap-timeout.patch
# removed due to #759334
#Patch38: cyrus-sasl-2.1.23-pam_rhosts.patch
Patch42: cyrus-sasl-2.1.26-relro.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=816250
Patch43: cyrus-sasl-2.1.26-null-crypt.patch
Patch44: cyrus-sasl-2.1.26-release-server_creds.patch
# AM_CONFIG_HEADER is obsolete, use AC_CONFIG_HEADERS instead
Patch45: cyrus-sasl-2.1.26-obsolete-macro.patch
# missing size_t declaration in sasl.h
Patch46: cyrus-sasl-2.1.26-size_t.patch
# disable incorrect check for MkLinux
Patch47: cyrus-sasl-2.1.26-ppc.patch
# detect gsskrb5_register_acceptor_identity macro (#976538)
Patch48: cyrus-sasl-2.1.26-keytab.patch
Patch49: cyrus-sasl-2.1.26-md5global.patch
# revert upstream commit 080e51c7fa0421eb2f0210d34cf0ac48a228b1e9 (#984079)
# https://bugzilla.cyrusimap.org/show_bug.cgi?id=3480
Patch50: cyrus-sasl-2.1.26-revert-upstream-080e51c7fa0421eb2f0210d34cf0ac48a228b1e9.patch
# improve sql libraries detection
Patch51: cyrus-sasl-2.1.26-sql.patch
# improve configuration error message
Patch52: cyrus-sasl-2.1.26-config-error.patch
# Treat SCRAM-SHA-1/DIGEST-MD5 as more secure than PLAIN (#970718)
Patch53: cyrus-sasl-2.1.26-prefer-SCRAM-SHA-1-over-PLAIN.patch
# Do not leak memory in sample server (#852755)
Patch54: cyrus-sasl-2.1.26-sample-leak.patch
# Document ability to run saslauthd unprivileged (#1189203)
Patch55: cyrus-sasl-2.1.26-saslauthd-user.patch
# Too much loogging in GSSAPI resolved (#1187097)
Patch56: cyrus-sasl-2.1.26-user-specified-logging.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool, gdbm-devel, groff
BuildRequires: krb5-devel >= 1.2.2, openssl-devel, pam-devel, pkgconfig
BuildRequires: zlib-devel
BuildRequires: libdb-devel
%if ! %{bootstrap_cyrus_sasl}
BuildRequires: openldap-devel
%endif
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd systemd-units
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel systemd-units
Requires: /sbin/nologin
Provides: user(%username)
Provides: group(%username)


%description
The %{name} package contains the Cyrus implementation of SASL.
SASL is the Simple Authentication and Security Layer, a method for
adding authentication support to connection-based protocols.

%package lib
Summary: Shared libraries needed by applications which use Cyrus SASL

%description lib
The %{name}-lib package contains shared libraries which are needed by
applications which use the Cyrus SASL library.

%package devel
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Summary: Files needed for developing applications with Cyrus SASL

%description devel
The %{name}-devel package contains files needed for developing and
compiling applications which use the Cyrus SASL library.

%package gssapi
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: GSSAPI authentication support for Cyrus SASL

%description gssapi
The %{name}-gssapi package contains the Cyrus SASL plugins which
support GSSAPI authentication. GSSAPI is commonly used for Kerberos
authentication.

%package plain
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: PLAIN and LOGIN authentication support for Cyrus SASL

%description plain
The %{name}-plain package contains the Cyrus SASL plugins which support
PLAIN and LOGIN authentication schemes.

%package md5
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: CRAM-MD5 and DIGEST-MD5 authentication support for Cyrus SASL

%description md5
The %{name}-md5 package contains the Cyrus SASL plugins which support
CRAM-MD5 and DIGEST-MD5 authentication schemes.

%package ntlm
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: NTLM authentication support for Cyrus SASL

%description ntlm
The %{name}-ntlm package contains the Cyrus SASL plugin which supports
the NTLM authentication scheme.

# This would more appropriately be named cyrus-sasl-auxprop-sql.
%package sql
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: SQL auxprop support for Cyrus SASL

%description sql
The %{name}-sql package contains the Cyrus SASL plugin which supports
using a RDBMS for storing shared secrets.

%if ! %{bootstrap_cyrus_sasl}
# This was *almost* named cyrus-sasl-auxprop-ldapdb, but that's a lot of typing.
%package ldap
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: LDAP auxprop support for Cyrus SASL

%description ldap
The %{name}-ldap package contains the Cyrus SASL plugin which supports using
a directory server, accessed using LDAP, for storing shared secrets.
%endif

%package scram
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: SCRAM auxprop support for Cyrus SASL

%description scram
The %{name}-scram package contains the Cyrus SASL plugin which supports
the SCRAM authentication scheme.

%package gs2
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: GS2 support for Cyrus SASL

%description gs2
The %{name}-gs2 package contains the Cyrus SASL plugin which supports
the GS2 authentication scheme.

###


%prep
%setup -q
chmod -x doc/*.html
chmod -x include/*.h
%patch11 -p1 -b .no_rpath
%patch15 -p1 -b .path
%patch23 -p1 -b .man
%patch24 -p1 -b .sizes
%patch31 -p1 -b .krb4
%patch32 -p1 -b .warnings
%patch34 -p1 -b .ldap-timeout
%patch42 -p1 -b .relro
%patch43 -p1 -b .null-crypt
%patch44 -p1 -b .release-server_creds
%patch45 -p1 -b .obsolete-macro
%patch46 -p1 -b .size_t
%patch47 -p1 -b .ppc
%patch48 -p1 -b .keytab
%patch49 -p1 -b .md5global.h
%patch50 -p1 -b .gssapi
%patch51 -p1 -b .sql
%patch52 -p1 -b .configerr
%patch53 -p1 -b .sha1vsplain
%patch54 -p1 -b .leak
%patch55 -p1 -b .man-unprivileged
%patch56 -p1 -b .too-much-logging


%build
# Find Kerberos.
krb5_prefix=`krb5-config --prefix`
if test x$krb5_prefix = x%{_prefix} ; then
        krb5_prefix=
else
        CPPFLAGS="-I${krb5_prefix}/include $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="-L${krb5_prefix}/%{_lib} $LDFLAGS"; export LDFLAGS
fi

# Find OpenSSL.
LIBS="-lcrypt"; export LIBS
if pkg-config openssl ; then
        CPPFLAGS="`pkg-config --cflags-only-I openssl` $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="`pkg-config --libs-only-L openssl` $LDFLAGS"; export LDFLAGS
fi

# Patch config.sub to support ppc64p7 subarch (Fedora specific)
# This is similar to what the config.sub from automake has
for i in `find . -name config.sub`; do
  perl -pi -e "s/ppc64-\*/ppc64-\* \| ppc64p7-\*/" $i
done

CFLAGS="$RPM_OPT_FLAGS $CFLAGS $CPPFLAGS -fPIE"; export CFLAGS
LDFLAGS="$LDFLAGS -pie -Wl,-z,now"; export LDFLAGS

echo "$CFLAGS"
echo "$CPPFLAGS"
echo "$LDFLAGS"

%configure \
        --enable-shared --disable-static \
        --disable-java \
        --with-plugindir=%{_plugindir2} \
        --with-configdir=%{_plugindir2}:%{_sysconfdir}/sasl2 \
        --disable-krb4 \
        --enable-gssapi${krb5_prefix:+=${krb5_prefix}} \
        --with-gss_impl=mit \
        --with-rc4 \
        --with-dblib=berkeley \
        --with-bdb=db \
        --with-saslauthd=/run/saslauthd --without-pwcheck \
%if ! %{bootstrap_cyrus_sasl}
        --with-ldap \
%endif
        --with-devrandom=/dev/urandom \
        --enable-anon \
        --enable-cram \
        --enable-digest \
        --enable-ntlm \
        --enable-plain \
        --enable-login \
        --enable-alwaystrue \
        --enable-httpform \
        --disable-otp \
%if ! %{bootstrap_cyrus_sasl}
        --enable-ldapdb \
%endif
        --enable-sql --with-mysql=no --with-pgsql=no \
        --without-sqlite \
        "$@"
        # --enable-auth-sasldb -- EXPERIMENTAL
make sasldir=%{_plugindir2}
make -C saslauthd testsaslauthd
make -C sample

# Build a small program to list the available mechanisms, because I need it.
pushd lib
../libtool --mode=link %{__cc} -o sasl2-shared-mechlist -I../include $CFLAGS %{SOURCE7} $LDFLAGS ./libsasl2.la


%install
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2}
make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2} -C plugins

install -m755 -d $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install \
install -m755 sample/client $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-client
./libtool --mode=install \
install -m755 sample/server $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-server
./libtool --mode=install \
install -m755 saslauthd/testsaslauthd $RPM_BUILD_ROOT%{_sbindir}/testsaslauthd

# Install the saslauthd mdoc page in the expected location.  Sure, it's not
# really a man page, but groff seems to be able to cope with it.
install -m755 -d $RPM_BUILD_ROOT%{_mandir}/man8/
install -m644 -p saslauthd/saslauthd.mdoc $RPM_BUILD_ROOT%{_mandir}/man8/saslauthd.8
install -m644 -p saslauthd/testsaslauthd.8 $RPM_BUILD_ROOT%{_mandir}/man8/testsaslauthd.8

# Create the saslauthd listening directory.
install -m755 -d $RPM_BUILD_ROOT/run/saslauthd

# Install the init script for saslauthd and the init script's config file.
install -m755 -d $RPM_BUILD_ROOT/etc/rc.d/init.d $RPM_BUILD_ROOT/etc/sysconfig
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 -p %{SOURCE5} $RPM_BUILD_ROOT/%{_unitdir}/saslauthd.service
install -m644 -p %{SOURCE9} $RPM_BUILD_ROOT/etc/sysconfig/saslauthd
install -m755 -d $RPM_BUILD_ROOT/%{_tmpfilesdir}
install -m644 -p %{SOURCE11} $RPM_BUILD_ROOT/%{_tmpfilesdir}/saslauthd.conf

# Install the config dirs if they're not already there.
install -m755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/sasl2
install -m755 -d $RPM_BUILD_ROOT/%{_plugindir2}

# Provide an easy way to query the list of available mechanisms.
./libtool --mode=install \
install -m755 lib/sasl2-shared-mechlist $RPM_BUILD_ROOT/%{_sbindir}/

# Remove unpackaged files from the buildroot.
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/libotp.*
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_mandir}/cat8/saslauthd.8


%clean
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

%pre
getent group %{username} >/dev/null || groupadd -g 76 -r %{username}
getent passwd %{username} >/dev/null || useradd -r -g %{username} -d %{homedir} -s /sbin/nologin -c "%{hint}" %{username}

%post
%systemd_post saslauthd.service

%preun
%systemd_preun saslauthd.service

%postun
%systemd_postun_with_restart saslauthd.service

%post lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc saslauthd/LDAP_SASLAUTHD
%{_mandir}/man8/*
%{_sbindir}/pluginviewer
%{_sbindir}/saslauthd
%{_sbindir}/testsaslauthd
%config(noreplace) /etc/sysconfig/saslauthd
%{_unitdir}/saslauthd.service
%{_tmpfilesdir}/saslauthd.conf
%dir %attr(0775, root, saslauth) /run/saslauthd

%files lib
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README doc/*.html
%{_libdir}/libsasl*.so.*
%dir %{_sysconfdir}/sasl2
%dir %{_plugindir2}/
%{_plugindir2}/*anonymous*.so*
%{_plugindir2}/*sasldb*.so*
%{_sbindir}/saslpasswd2
%{_sbindir}/sasldblistusers2

%files plain
%defattr(-,root,root)
%{_plugindir2}/*plain*.so*
%{_plugindir2}/*login*.so*

%if ! %{bootstrap_cyrus_sasl}
%files ldap
%defattr(-,root,root)
%{_plugindir2}/*ldapdb*.so*
%endif

%files md5
%defattr(-,root,root)
%{_plugindir2}/*crammd5*.so*
%{_plugindir2}/*digestmd5*.so*

%files ntlm
%defattr(-,root,root)
%{_plugindir2}/*ntlm*.so*

%files sql
%defattr(-,root,root)
%{_plugindir2}/*sql*.so*

%files gssapi
%defattr(-,root,root)
%{_plugindir2}/*gssapi*.so*

%files scram
%defattr(-,root,root)
%{_plugindir2}/libscram.so*

%files gs2
%defattr(-,root,root)
%{_plugindir2}/libgs2.so*

%files devel
%defattr(-,root,root)
%doc doc/*.txt
%{_bindir}/sasl2-sample-client
%{_bindir}/sasl2-sample-server
%{_includedir}/*
%{_libdir}/libsasl*.*so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_sbindir}/sasl2-shared-mechlist

%changelog
* Fri Oct 23 2015 cjacker - 2.1.26-25
- Rebuild for new 4.0 release

