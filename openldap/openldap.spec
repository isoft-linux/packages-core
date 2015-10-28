#NOTE: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#we only build client library of openldap for our DESKTOP!!!!!!!!!!!!

%global systemctl_bin /usr/bin/systemctl
Name: openldap
Version: 2.4.40
Release: 13
Summary: LDAP support libraries
License: OpenLDAP
URL: http://www.openldap.org/
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source4: ldap.conf

# patches for 2.4
Patch0: openldap-manpages.patch
Patch1: openldap-sql-linking.patch
Patch2: openldap-reentrant-gethostby.patch
Patch3: openldap-smbk5pwd-overlay.patch
Patch4: openldap-man-sasl-nocanon.patch
Patch5: openldap-ai-addrconfig.patch

# GCC 5 cpp patch, pending upstream inclusion (ITS #8056)
Patch101: openldap-gcc-5.patch

BuildRequires: cyrus-sasl-devel, nss-devel, krb5-devel, tcp_wrappers-devel
BuildRequires: glibc-devel, libtool, libtool-ltdl-devel, groff, perl, perl-devel, perl(ExtUtils::Embed)
# smbk5pwd overlay:
BuildRequires: openssl-devel
Requires: nss-tools

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Requires: openldap%{?_isa} = %{version}-%{release}, cyrus-sasl-devel%{?_isa}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package clients
Summary: LDAP client utilities
Requires: openldap%{?_isa} = %{version}-%{release}

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

%prep
%setup

%patch101 -p1

AUTOMAKE=%{_bindir}/true autoreconf -fi

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build

%ifarch s390 s390x
  export CFLAGS="-fPIE"
%else
  export CFLAGS="-fpie"
%endif
export LDFLAGS="-pie"
# avoid stray dependencies (linker flag --as-needed)
# enable experimental support for LDAP over UDP (LDAP_CONNECTIONLESS)
export CFLAGS="${CFLAGS} %{optflags} -Wl,--as-needed,-z,relro,-z,now -DLDAP_CONNECTIONLESS"

%configure \
    --disable-static  \
    --enable-dynamic  \
    --disable-debug   \
    --disable-slapd \
    --with-cyrus-sasl \
    --without-fetch \
    --with-threads \
    --with-pic
make depend
make %{_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/

make install DESTDIR=%{buildroot} STRIP=""

# setup data and runtime directories
mkdir -p %{buildroot}%{_sharedstatedir}
install -m 0700 -d %{buildroot}%{_sharedstatedir}/ldap

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# re-symlink unversioned libraries, so ldconfig is not confused
pushd %{buildroot}%{_libdir}
v=%{version}
version=$(echo ${v%.[0-9]*})
for lib in liblber libldap libldap_r; do
	rm -f ${lib}.so
	ln -s ${lib}-${version}.so.2 ${lib}.so
done
popd

# tweak permissions on the libraries to make sure they're correct
chmod 0755 %{buildroot}%{_libdir}/lib*.so*
chmod 0644 %{buildroot}%{_libdir}/lib*.*a


#remove server man pages
rm -rf %{buildroot}%{_mandir}/man8
rm -rf %{buildroot}%{_mandir}/man5/slapd*.5*
rm -rf %{buildroot}%{_mandir}/man5/slapo-*.5*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_sysconfdir}/openldap
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%{_libdir}/liblber-2.4*.so.*
%{_libdir}/libldap-2.4*.so.*
%{_libdir}/libldap_r-2.4*.so.*
%{_mandir}/man5/ldif.5*
%{_mandir}/man5/ldap.conf.5*

%files clients
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 2.4.40-13
- Rebuild for new 4.0 release

