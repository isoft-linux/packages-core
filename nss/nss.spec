%global nspr_version 4.10.8
%global nss_util_version 3.19.2
%global nss_softokn_version 3.19.2
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global allTools "certutil cmsutil crlutil derdump modutil pk12util signtool signver ssltap vfychain vfyserv"

# solution taken from icedtea-web.spec
%define multilib_arches %{power64} sparc64 x86_64
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif

# Define if using a source archive like "nss-version.with.ckbi.version".
# To "disable", add "#" to start of line, AND a space after "%".
#% define nss_ckbi_suffix .with.ckbi.1.93

Summary:          Network Security Services
Name:             nss
Version:          3.19.2
# for Rawhide, please always use release >= 2
# for Fedora release branches, please use release < 2 (1.0, 1.1, ...)
Release:          3%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
# TODO: revert to same version as nss once we are done with the merge
Requires:         nss-softokn%{_isa} >= %{nss_softokn_version}
Requires:         nss-system-init
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
# TODO: revert to same version as nss once we are done with the merge
# Using '>=' but on RHEL the requires should be '='
BuildRequires:    nss-softokn-devel >= %{nss_softokn_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl

%{!?nss_ckbi_suffix:%define full_nss_version %{version}}
%{?nss_ckbi_suffix:%define full_nss_version %{version}%{nss_ckbi_suffix}}

Source0:          %{name}-%{full_nss_version}.tar.gz
Source1:          nss.pc.in
Source2:          nss-config.in
Source3:          blank-cert8.db
Source4:          blank-key3.db
Source5:          blank-secmod.db
Source6:          blank-cert9.db
Source7:          blank-key4.db
Source8:          system-pkcs11.txt
Source9:          setup-nsssysinit.sh
Source12:         %{name}-pem-20140125.tar.bz2
Source20:         nss-config.xml
Source21:         setup-nsssysinit.xml
Source22:         pkcs11.txt.xml
Source23:         cert8.db.xml
Source24:         cert9.db.xml
Source25:         key3.db.xml
Source26:         key4.db.xml
Source27:         secmod.db.xml

Patch2:           add-relro-linker-option.patch
Patch3:           renegotiate-transitional.patch
Patch6:           nss-enable-pem.patch
Patch16:          nss-539183.patch
# must statically link pem against the freebl in the buildroot
# Needed only when freebl on tree has new APIS
Patch25:          nsspem-use-system-freebl.patch
# TODO: Remove this patch when the ocsp test are fixed
Patch40:          nss-3.14.0.0-disble-ocsp-test.patch
# Fedora / RHEL-only patch, the templates directory was originally introduced to support mod_revocator
Patch47:          utilwrap-include-templates.patch
# TODO remove when we switch to building nss without softoken
Patch49:          nss-skip-bltest-and-fipstest.patch
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list of list of directories
# to be searched for for header files. This ensures a build even when system 
# headers are older. Such is the case when starting an update with API changes or even private export changes.
# Once the buildroot aha been bootstrapped the patch may be removed but it doesn't hurt to keep it.
Patch50:          iquote.patch
Patch52:          disableSSL2libssl.patch
Patch53:          disableSSL2tests.patch
# fix upstream bug 1151037, until we rebase to 3.19


Patch54:         nss-disable-fips-test.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.

%package sysinit
Summary:          System NSS Initialization
Group:            System Environment/Base
# providing nss-system-init without version so that it can
# be replaced by a better one, e.g. supplied by the os vendor
Provides:         nss-system-init
Requires:         nss = %{version}-%{release}
Requires(post):   coreutils, sed

%description sysinit
Default Operating System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Provides:         nss-static = %{version}-%{release}
Requires:         nss = %{version}-%{release}
Requires:         nss-util-devel
Requires:         nss-softokn-devel
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkgconfig
BuildRequires:    xmlto

%description devel
Header and Library files for doing development with Network Security Services.


%package pkcs11-devel
Summary:          Development libraries for PKCS #11 (Cryptoki) using NSS
Group:            Development/Libraries
Provides:         nss-pkcs11-devel-static = %{version}-%{release}
Requires:         nss-devel = %{version}-%{release}
Requires:         nss-softokn-freebl-devel >= %{nss_softokn_version}

%description pkcs11-devel
Library files for developing PKCS #11 modules using basic NSS 
low level services.


%prep
%setup -q
%setup -q -T -D -n %{name}-%{version} -a 12

%patch2 -p0 -b .relro
%patch3 -p0 -b .transitional
%patch6 -p0 -b .libpem
%patch16 -p0 -b .539183
# link pem against buildroot's freebl, essential when mixing and matching
%patch25 -p0 -b .systemfreebl
%patch40 -p0 -b .noocsptest
%patch47 -p0 -b .templates
%patch49 -p0 -b .skipthem
%patch50 -p0 -b .iquote
pushd nss
%patch52 -p1 -b .disableSSL2libssl
%patch53 -p1 -b .disableSSL2tests
popd
%patch54 -p1


#########################################################
# Higher-level libraries and test tools need access to
# module-private headers from util, freebl, and softoken
# until fixed upstream we must copy some headers locally
#########################################################

pemNeedsFromSoftoken="lowkeyi lowkeyti softoken softoknt"
for file in ${pemNeedsFromSoftoken}; do
    %{__cp} ./nss/lib/softoken/${file}.h ./nss/lib/ckfw/pem/
done

# Copying these header until the upstream bug is accepted
# Upstream https://bugzilla.mozilla.org/show_bug.cgi?id=820207
%{__cp} ./nss/lib/softoken/lowkeyi.h ./nss/cmd/rsaperf
%{__cp} ./nss/lib/softoken/lowkeyti.h ./nss/cmd/rsaperf

##### Remove util/freebl/softoken and low level tools
######## Remove freebl, softoken and util
%{__rm} -rf ./nss/lib/freebl
%{__rm} -rf ./nss/lib/softoken
%{__rm} -rf ./nss/lib/util
######## Remove nss-softokn test tools as we already ran
# the cipher test suite as part of the nss-softokn build
%{__rm} -rf ./nss/cmd/bltest
%{__rm} -rf ./nss/cmd/fipstest
%{__rm} -rf ./nss/cmd/rsaperf_low

pushd nss/tests/ssl
# Create versions of sslcov.txt and sslstress.txt that disable tests
# for SSL2 and EXPORT ciphers.
cat sslcov.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslcov.noSSL2orExport.txt
cat sslstress.txt| sed -r "s/^([^#].*EXPORT|^[^#].*SSL2)/#disabled \1/" > sslstress.noSSL2orExport.txt
popd

%build

export NSS_NO_SSL2_NO_EXPORT=1

NSS_NO_PKCS11_BYPASS=1
export NSS_NO_PKCS11_BYPASS

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=%{_libdir}

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSSUTIL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
export NSSUTIL_LIB_DIR=%{_libdir}

export FREEBL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-softokn | sed 's/-I//'`
export FREEBL_LIB_DIR=%{_libdir}
export USE_SYSTEM_FREEBL=1
# FIXME choose one or the other style and submit a patch upstream
# wtc has suggested using NSS_USE_SYSTEM_FREEBL
export NSS_USE_SYSTEM_FREEBL=1

export FREEBL_LIBS=`/usr/bin/pkg-config --libs nss-softokn`

export SOFTOKEN_LIB_DIR=%{_libdir}
# use the system ones
export USE_SYSTEM_NSSUTIL=1
export USE_SYSTEM_SOFTOKEN=1

# tell the upstream build system what we are doing
export NSS_BUILD_WITHOUT_SOFTOKEN=1

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE

%ifarch x86_64 %{power64} ia64 s390x sparc64 aarch64
USE_64=1
export USE_64
%endif

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

##### phase 2: build the rest of nss
# nss supports pluggable ecc with more than suite-b
NSS_ECC_MORE_THAN_SUITE_B=1
export NSS_ECC_MORE_THAN_SUITE_B

export NSS_BLTEST_NOT_AVAILABLE=1
%{__make} -C ./nss/coreconf
%{__make} -C ./nss/lib/dbm
%{__make} -C ./nss
unset NSS_BLTEST_NOT_AVAILABLE

# build the man pages clean
pushd ./nss
%{__make} clean_docs build_docs
popd

# and copy them to the dist directory for %%install to find them
%{__mkdir_p} ./dist/docs/nroff
%{__cp} ./nss/doc/nroff/* ./dist/docs/nroff

# Set up our package file
# The nspr_version and nss_{util|softokn}_version globals used
# here match the ones nss has for its Requires. 
# Using the current %%{nss_softokn_version}
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{nss_softokn_version},g" > \
                          ./dist/pkgconfig/nss.pc

NSS_VMAJOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

export NSS_VMAJOR
export NSS_VMINOR
export NSS_VPATCH

%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > ./dist/pkgconfig/nss-config

chmod 755 ./dist/pkgconfig/nss-config

%{__cat} %{SOURCE9} > ./dist/pkgconfig/setup-nsssysinit.sh
chmod 755 ./dist/pkgconfig/setup-nsssysinit.sh

%{__cp} ./nss/lib/ckfw/nssck.api ./dist/private/nss/

date +"%e %B %Y" | tr -d '\n' > date.xml
echo -n %{version} > version.xml

# configuration files and setup script
for m in %{SOURCE20} %{SOURCE21} %{SOURCE22}; do
  cp ${m} .
done
for m in nss-config.xml setup-nsssysinit.xml pkcs11.txt.xml; do
  xmlto man ${m}
done

# nss databases considered to be configuration files
for m in %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}; do
  cp ${m} .
done
for m in cert8.db.xml cert9.db.xml key3.db.xml key4.db.xml secmod.db.xml; do
  xmlto man ${m}
done
 

%check
if [ ${DISABLETEST:-0} -eq 1 ]; then
  echo "testing disabled"
  exit 0
fi

# Begin -- copied from the build section

# inform the ssl test scripts that SSL2 is disabled
export NSS_NO_SSL2_NO_EXPORT=1

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

BUILD_OPT=1
export BUILD_OPT

%ifarch x86_64 %{power64} ia64 s390x sparc64 aarch64
USE_64=1
export USE_64
%endif

export NSS_BLTEST_NOT_AVAILABLE=1

export NSS_TEST_DISABLE_FIPS=1

# needed for the fips manging test
export SOFTOKEN_LIB_DIR=%{_libdir}

# End -- copied from the build section

# enable the following line to force a test failure
# find ./nss -name \*.chk | xargs rm -f

# Run test suite.
# In order to support multiple concurrent executions of the test suite
# (caused by concurrent RPM builds) on a single host,
# we'll use a random port. Also, we want to clean up any stuck
# selfserv processes. If process name "selfserv" is used everywhere,
# we can't simply do a "killall selfserv", because it could disturb
# concurrent builds. Therefore we'll do a search and replace and use
# a different process name.
# Using xargs doesn't mix well with spaces in filenames, in order to
# avoid weird quoting we'll require that no spaces are being used.

SPACEISBAD=`find ./nss/tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi
MYRAND=`perl -e 'print 9000 + int rand 1000'`; echo $MYRAND ||:
RANDSERV=selfserv_${MYRAND}; echo $RANDSERV ||:
DISTBINDIR=`ls -d ./dist/*.OBJ/bin`; echo $DISTBINDIR ||:
pushd `pwd`
cd $DISTBINDIR
ln -s selfserv $RANDSERV
popd
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find ./nss/tests -type f |\
  grep -v "\.db$" |grep -v "\.crl$" | grep -v "\.crt$" |\
  grep -vw CVS  |xargs grep -lw selfserv |\
  xargs -l perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall $RANDSERV || :

rm -rf ./tests_results
pushd ./nss/tests/
# all.sh is the test suite script

#  don't need to run all the tests when testing packaging
#  nss_cycles: standard pkix upgradedb sharedb
#nss_tests="libpkix cert dbtests tools fips sdr crmf smime ssl ocsp merge pkits chains"

#we disable fipsmode
nss_tests="libpkix cert dbtests tools sdr crmf smime ssl ocsp merge pkits chains"
#  nss_ssl_tests: crl bypass_normal normal_bypass normal_fips fips_normal iopr
#  nss_ssl_run: cov auth stress
#
# Uncomment these lines if you need to temporarily
# disable some test suites for faster test builds
nss_ssl_tests="crl bypass_normal normal_bypass iopr"
nss_ssl_run="cov auth"

SKIP_NSS_TEST_SUITE=`echo $SKIP_NSS_TEST_SUITE`

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh
else
  echo "skipped test suite"
fi

popd

# Normally, the grep exit status is 0 if selected lines are found and 1 otherwise,
# Grep exits with status greater than 1 if an error ocurred. 
# If there are test failures we expect TEST_FAILURES > 0 and GREP_EXIT_STATUS = 0, 
# With no test failures we expect TEST_FAILURES = 0 and GREP_EXIT_STATUS = 1, whereas 
# GREP_EXIT_STATUS > 1 would indicate an error in grep such as failure to find the log file.
killall $RANDSERV || :

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  TEST_FAILURES=$(grep -c FAILED ./tests_results/security/localhost.1/output.log) || GREP_EXIT_STATUS=$?
else
  TEST_FAILURES=0
  GREP_EXIT_STATUS=1
fi

if [ ${GREP_EXIT_STATUS:-0} -eq 1 ]; then
  echo "okay: test suite detected no failures"
else
  if [ ${GREP_EXIT_STATUS:-0} -eq 0 ]; then
    # while a situation in which grep return status is 0 and it doesn't output
    # anything shouldn't happen, set the default to something that is
    # obviously wrong (-1)
    echo "error: test suite had ${TEST_FAILURES:--1} test failure(s)"
    exit 1
  else
    if [ ${GREP_EXIT_STATUS:-0} -eq 2 ]; then
      echo "error: grep has not found log file"
      exit 1
    else
      echo "error: grep failed with exit code: ${GREP_EXIT_STATUS}"
      exit 1
    fi
  fi
fi
echo "test suite completed"

%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
# because of the pp.1 conflict with perl-PAR-Packer
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5

touch $RPM_BUILD_ROOT%{_libdir}/libnssckbi.so
%{__install} -p -m 755 dist/*.OBJ/lib/libnssckbi.so $RPM_BUILD_ROOT/%{_libdir}/nss/libnssckbi.so

# Copy the binary libraries we want
for file in libnss3.so libnsspem.so libnsssysinit.so libsmime3.so libssl3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Install the empty NSS db files
# Legacy db
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
%{__install} -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
%{__install} -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.db
# Shared db
%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert9.db
%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key4.db
%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/pkcs11.txt

# Copy the development libraries we want
for file in libcrmf.a libnssb.a libnssckfw.a
do
  %{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump ocspclnt pp selfserv strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the template files we want
for file in dist/private/nss/nssck.api
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3/templates
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-config $RPM_BUILD_ROOT/%{_bindir}/nss-config
# Copy the pkcs #11 configuration script
%{__install} -p -m 755 ./dist/pkgconfig/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh
# install a symbolic link to it, without the ".sh" suffix,
# that matches the man page documentation
ln -r -s -f $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit.sh $RPM_BUILD_ROOT/%{_bindir}/setup-nsssysinit

# Copy the man pages for scripts
for f in nss-config setup-nsssysinit; do 
   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
# Copy the man pages for the nss tools
for f in "%{allTools}"; do 
  install -c -m 644 ./dist/docs/nroff/${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
install -c -m 644 ./dist/docs/nroff/pp.1 $RPM_BUILD_ROOT%{_datadir}/doc/nss-tools/pp.1

# Copy the man pages for the configuration files
for f in pkcs11.txt; do 
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done
# Copy the man pages for the nss databases
for f in cert8.db cert9.db key3.db key4.db secmod.db; do 
   install -c -m 644 ${f}.5 $RPM_BUILD_ROOT%{_mandir}/man5/${f}.5
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%triggerpostun -n nss-sysinit -- nss-sysinit < 3.12.8-3
# Reverse unwanted disabling of sysinit by faulty preun sysinit scriplet
# from previous versions of nss.spec
/usr/bin/setup-nsssysinit.sh on

%post
# If we upgrade, and the shared filename is a regular file, then we must
# remove it, before we can install the alternatives symbolic link.
if [ $1 -gt 1 ] ; then
  # when upgrading or downgrading
  if ! test -L %{_libdir}/libnssckbi.so; then
    rm -f %{_libdir}/libnssckbi.so
  fi
fi
# Install the symbolic link
# FYI: Certain other packages use alternatives --set to enforce that the first
# installed package is preferred. We don't do that. Highest priority wins.
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
  %{alt_ckbi} %{_libdir}/nss/libnssckbi.so 10
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
  # package removal
  %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
else
  # upgrade or downgrade
  # If the new installed package uses a regular file (not a symblic link),
  # then cleanup the alternatives link.
  if ! test -L %{_libdir}/libnssckbi.so; then
    %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/nss/libnssckbi.so
  fi
fi
/sbin/ldconfig

%posttrans
# An earlier version of this package had an incorrect %%postun script (3.14.3-9).
# (The incorrect %%postun always called "update-alternatives --remove",
# because it incorrectly assumed that test -f returns false for symbolic links.)
# The only possible remedy to fix the mistake that "always removes on upgrade"
# made by the older %%postun script, is to repair it in %%posttrans of the new package.
# Strategy:
# %%posttrans is never called when uninstalling.
# %%posttrans is only called when installing or upgrading a package.
# Because %%posttrans is the very last action of a package install,
# %%{_libdir}/libnssckbi.so must exist.
# If it does not, it's the result of the incorrect removal from a broken %%postun.
# In this case, we repeat installation of the alternatives link.
if ! test -e %{_libdir}/libnssckbi.so; then
  %{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
    %{alt_ckbi} %{_libdir}/nss/libnssckbi.so 10
fi


%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license nss/COPYING
%{_libdir}/libnss3.so
%{_libdir}/libssl3.so
%{_libdir}/libsmime3.so
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/nss/libnssckbi.so
%{_libdir}/libnsspem.so
%dir %{_sysconfdir}/pki/nssdb
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert8.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key3.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/secmod.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/cert9.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/key4.db
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pki/nssdb/pkcs11.txt
%attr(0644,root,root) %doc %{_mandir}/man5/cert8.db.5.gz
%attr(0644,root,root) %doc %{_mandir}/man5/key3.db.5.gz
%attr(0644,root,root) %doc %{_mandir}/man5/secmod.db.5.gz
%attr(0644,root,root) %doc %{_mandir}/man5/cert9.db.5.gz
%attr(0644,root,root) %doc %{_mandir}/man5/key4.db.5.gz
%attr(0644,root,root) %doc %{_mandir}/man5/pkcs11.txt.5.gz

%files sysinit
%defattr(-,root,root)
%{_libdir}/libnsssysinit.so
%{_bindir}/setup-nsssysinit.sh
# symbolic link to setup-nsssysinit.sh
%{_bindir}/setup-nsssysinit
%attr(0644,root,root) %doc %{_mandir}/man1/setup-nsssysinit.1.gz

%files tools
%defattr(-,root,root)
%{_bindir}/certutil
%{_bindir}/cmsutil
%{_bindir}/crlutil
%{_bindir}/modutil
%{_bindir}/pk12util
%{_bindir}/signtool
%{_bindir}/signver
%{_bindir}/ssltap
%{unsupported_tools_directory}/atob
%{unsupported_tools_directory}/btoa
%{unsupported_tools_directory}/derdump
%{unsupported_tools_directory}/ocspclnt
%{unsupported_tools_directory}/pp
%{unsupported_tools_directory}/selfserv
%{unsupported_tools_directory}/strsclnt
%{unsupported_tools_directory}/symkeyutil
%{unsupported_tools_directory}/tstclnt
%{unsupported_tools_directory}/vfyserv
%{unsupported_tools_directory}/vfychain
# instead of %%{_mandir}/man*/* let's list them explicitely
# supported tools
%attr(0644,root,root) %doc %{_mandir}/man1/certutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/cmsutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/crlutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/modutil.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/pk12util.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/signtool.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/signver.1.gz
# unsupported tools
%attr(0644,root,root) %doc %{_mandir}/man1/derdump.1.gz
%dir %{_datadir}/doc/nss-tools
%attr(0644,root,root) %doc %{_datadir}/doc/nss-tools/pp.1
%attr(0644,root,root) %doc %{_mandir}/man1/ssltap.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/vfychain.1.gz
%attr(0644,root,root) %doc %{_mandir}/man1/vfyserv.1.gz

%files devel
%defattr(-,root,root)
%{_libdir}/libcrmf.a
%{_libdir}/pkgconfig/nss.pc
%{_bindir}/nss-config
%attr(0644,root,root) %doc %{_mandir}/man1/nss-config.1.gz

%dir %{_includedir}/nss3
%{_includedir}/nss3/cert.h
%{_includedir}/nss3/certdb.h
%{_includedir}/nss3/certt.h
%{_includedir}/nss3/cmmf.h
%{_includedir}/nss3/cmmft.h
%{_includedir}/nss3/cms.h
%{_includedir}/nss3/cmsreclist.h
%{_includedir}/nss3/cmst.h
%{_includedir}/nss3/crmf.h
%{_includedir}/nss3/crmft.h
%{_includedir}/nss3/cryptohi.h
%{_includedir}/nss3/cryptoht.h
%{_includedir}/nss3/sechash.h
%{_includedir}/nss3/jar-ds.h
%{_includedir}/nss3/jar.h
%{_includedir}/nss3/jarfile.h
%{_includedir}/nss3/key.h
%{_includedir}/nss3/keyhi.h
%{_includedir}/nss3/keyt.h
%{_includedir}/nss3/keythi.h
%{_includedir}/nss3/nss.h
%{_includedir}/nss3/nssckbi.h
%{_includedir}/nss3/nsspem.h
%{_includedir}/nss3/ocsp.h
%{_includedir}/nss3/ocspt.h
%{_includedir}/nss3/p12.h
%{_includedir}/nss3/p12plcy.h
%{_includedir}/nss3/p12t.h
%{_includedir}/nss3/pk11func.h
%{_includedir}/nss3/pk11pqg.h
%{_includedir}/nss3/pk11priv.h
%{_includedir}/nss3/pk11pub.h
%{_includedir}/nss3/pk11sdr.h
%{_includedir}/nss3/pkcs12.h
%{_includedir}/nss3/pkcs12t.h
%{_includedir}/nss3/pkcs7t.h
%{_includedir}/nss3/preenc.h
%{_includedir}/nss3/secmime.h
%{_includedir}/nss3/secmod.h
%{_includedir}/nss3/secmodt.h
%{_includedir}/nss3/secpkcs5.h
%{_includedir}/nss3/secpkcs7.h
%{_includedir}/nss3/smime.h
%{_includedir}/nss3/ssl.h
%{_includedir}/nss3/sslerr.h
%{_includedir}/nss3/sslproto.h
%{_includedir}/nss3/sslt.h


%files pkcs11-devel
%defattr(-, root, root)
%{_includedir}/nss3/nssbase.h
%{_includedir}/nss3/nssbaset.h
%{_includedir}/nss3/nssckepv.h
%{_includedir}/nss3/nssckft.h
%{_includedir}/nss3/nssckfw.h
%{_includedir}/nss3/nssckfwc.h
%{_includedir}/nss3/nssckfwt.h
%{_includedir}/nss3/nssckg.h
%{_includedir}/nss3/nssckmdt.h
%{_includedir}/nss3/nssckt.h
%{_includedir}/nss3/templates/nssck.api
%{_libdir}/libnssb.a
%{_libdir}/libnssckfw.a


%changelog
