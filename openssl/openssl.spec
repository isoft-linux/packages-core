# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name:    openssl
Version: 1.0.2e
Release: 1
Epoch:   1
Source:  http://openssl.org/source/openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source6: make-dummy-cert
Source7: renew-dummy-cert

Source8:  openssl-thread-test.c
Source9:  opensslconf-new.h
Source10: opensslconf-new-warning.h

# Build changes
#Patch1: openssl-1.0.2c-rpmbuild.patch
Patch2: openssl-1.0.2a-defaults.patch
Patch5: openssl-1.0.2a-no-rpath.patch
Patch6: openssl-1.0.2a-test-use-localhost.patch
Patch7: openssl-1.0.0-timezone.patch
Patch8: openssl-1.0.1c-perlfind.patch
Patch9: openssl-1.0.1c-aliasing.patch

# Bug fixes
Patch23: openssl-1.0.2c-default-paths.patch
Patch24: openssl-1.0.2a-issuer-hash.patch

# Functionality changes
Patch33: openssl-1.0.0-beta4-ca-dir.patch
Patch34: openssl-1.0.2a-x509.patch

License: OpenSSL
URL: http://www.openssl.org/
BuildRequires: coreutils, perl, sed, zlib-devel, /usr/bin/cmp
BuildRequires: /usr/bin/rename
Requires: coreutils, make
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates >= 2008-5
# Needed obsoletes due to the base/lib subpackage split
Obsoletes: openssl < 1:1.0.1-0.3.beta3

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n %{name}-%{version}

#%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .defaults
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .perlfind
%patch9 -p1 -b .aliasing

%patch23 -p1 -b .default-paths
%patch24 -p1 -b .issuer-hash

%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

sslarch=%{_os}-%{_target_cpu}

./Configure \
	--prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/pki/tls \
    zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
    enable-cms enable-md2 no-mdc2 no-rc5 no-ec2m no-gost no-srp \
    shared  ${sslarch}

#modify libdir for x86_64
sed -i -e 's/LIBDIR=lib64/LIBDIR=lib/g' Makefile

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
make depend
make all

# Generate hashes for the included certs.
make rehash

%check
# Verify that what was compiled actually works.
# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}
make test

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs

mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/renew-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{_includedir}/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{_mandir}
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done

for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
done
popd

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc
mv CA.sh CA
popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc FAQ NEWS README
%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{_sysconfdir}/pki/tls/certs/renew-dummy-cert
%{_sysconfdir}/pki/tls/certs/Makefile
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%attr(0755,root,root) %{_bindir}/openssl
%attr(0644,root,root) %{_mandir}/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{_mandir}/man5*/*
%attr(0644,root,root) %{_mandir}/man7*/*

%files libs
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_libdir}/libcrypto.so.*
%attr(0755,root,root) %{_libdir}/libssl.so.*
%attr(0755,root,root) %{_libdir}/engines

%files devel
%defattr(-,root,root)
%doc doc/c-indentation.el doc/openssl.txt CHANGES
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*.a

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0644,root,root) %{_mandir}/man1*/*.pl*
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Fri Dec 04 2015 sulit <sulitsrc@gmail.com> - 1:1.0.2e-1
- update to 1.0.2e for security, and four securify fixes

* Fri Oct 23 2015 cjacker - 1:1.0.2d-3
- Rebuild for new 4.0 release

* Tue Jul 14 2015 Cjacker <cjacker@foxmail.com>
- update to 1.0.2d, fix security issue CVE-2015-1793.
