%global nspr_version 4.13.1
%global nss_name nss
%global nss_util_version 3.27.1
%global unsupported_tools_directory %{_libdir}/nss/unsupported-tools
%global saved_files_dir %{_libdir}/nss/saved

Summary:          Network Security Services Softoken Module
Name:             nss-softokn
Version:          3.27.1
Release:          1%{?dist}
License:          MPLv2.0
URL:              http://www.mozilla.org/projects/security/pki/nss/
Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
Requires:         nss-softokn-freebl%{_isa} >= %{version}-%{release}
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl

Source0:          %{name}-%{version}.tar.gz
# The nss-softokn tar ball is a subset of nss-{version}.tar.gz.
# We use the nss-split-softokn.sh script to keep only what we need
# via via nss-split-softokn.sh ${version}
# Detailed Steps:
# cd nss-softokn
# Split off nss-softokn out of the full nss source tar ball:
# sh ./nss-split-softokn.sh ${version}
# A file named {name}-{version}.tar.gz should appear
# which is ready for uploading to the lookaside cache.
Source1:          nss-split-softokn.sh
Source2:          nss-softokn.pc.in
Source3:          nss-softokn-config.in

# Select the tests to run based on the type of build
# This patch uses the gcc-iquote dir option documented at
# http://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
# to place the in-tree directories at the head of the list on list of directories
# to be searched for for header files. This ensures a build even when system freebl 
# headers are older. Such is the case when we are starting a major update.
# NSSUTIL_INCLUDE_DIR, after all, contains both util and freebl headers. 
# Once has been bootstapped the patch may be removed, but it doesn't hurt to keep it.
Patch10:           iquote.patch

# Patch adapted from rhel-7
# Upstream: https://bugzilla.mozilla.org/show_bug.cgi?id=1236720
Patch11: nss-softokn-add_encrypt_derive.patch

%description
Network Security Services Softoken Cryptographic Module

%package freebl
Summary:          Freebl library for the Network Security Services
Conflicts:        nss < 3.12.2.99.3-5
Conflicts:        prelink < 0.4.3
Conflicts:        filesystem < 3

%description freebl
NSS Softoken Cryptographic Module Freebl Library

Install the nss-softokn-freebl package if you need the freebl 
library.

%package freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
Provides:         nss-softokn-freebl-static = %{version}-%{release}
Requires:         nss-softokn-freebl%{?_isa} = %{version}-%{release}

%description freebl-devel
NSS Softoken Cryptographic Module Freebl Library Development Tools
This package supports special needs of some PKCS #11 module developers and
is otherwise considered private to NSS. As such, the programming interfaces
may change and the usual NSS binary compatibility commitments do not apply.
Developers should rely only on the officially supported NSS public API.

%package devel
Summary:          Development libraries for Network Security Services
Requires:         nss-softokn%{?_isa} = %{version}-%{release}
Requires:         nss-softokn-freebl-devel%{?_isa} = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         nss-util-devel >= %{nss_util_version}
Requires:         pkgconfig
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
# require nss at least the version when we split via subpackages

%description devel
Header and library files for doing development with Network Security Services.


%prep
%setup -q

# activate if needed when doing a major update with new apis
%patch10 -p0 -b .iquote
pushd nss
%patch11 -p0 -b .add_encrypt_derive
popd

%build

# partial RELRO support as a security enhancement
LDFLAGS+=-Wl,-z,relro
export LDFLAGS

FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

# Must export FREEBL_LOWHASH=1 for nsslowhash.h so that it gets
# copied to dist and the rpm install phase can find it
# This due of the upstream changes to fix
# https://bugzilla.mozilla.org/show_bug.cgi?id=717906
FREEBL_LOWHASH=1
export FREEBL_LOWHASH

export FREEBL_USE_PRELINK=1

# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

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
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

export NSSUTIL_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
export NSSUTIL_LIB_DIR=%{_libdir}

NSS_USE_SYSTEM_SQLITE=1
export NSS_USE_SYSTEM_SQLITE
export NSS_DISABLE_GTESTS=1

%ifnarch noarch
USE_64=1
export USE_64
%endif

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

# Use only the basicutil subset for sectools.a
export NSS_BUILD_SOFTOKEN_ONLY=1

# display processor information
CPU_INFO=`cat /proc/cpuinfo`
echo "############## CPU INFO ##################"
echo "${CPU_INFO}"
echo "##########################################"

# Compile softokn plus needed support
%{__make} -C ./nss/coreconf
%{__make} -C ./nss/lib/dbm

# ldvector.c, pkcs11.c, and lginit.c include nss/lib/util/verref.h, 
# which is private export, move it to where it can be found.
%{__mkdir_p} ./dist/private/nss
%{__mv} ./nss/lib/util/verref.h ./dist/private/nss/verref.h

%{__make} -C ./nss

# Set up our package file
# The nspr_version and nss_util_version globals used here
# must match the ones nss-softokn has for its Requires. 
%{__mkdir_p} ./dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" > \
                          ./dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

export SOFTOKEN_VMAJOR
export SOFTOKEN_VMINOR
export SOFTOKEN_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                          > ./dist/pkgconfig/nss-softokn-config

chmod 755 ./dist/pkgconfig/nss-softokn-config


%check

# Begin -- copied from the build section
FREEBL_NO_DEPEND=1
export FREEBL_NO_DEPEND

export BUILD_OPT=1

%ifnarch noarch
USE_64=1
export USE_64
%endif

# to test for the last tool built correctly
export NSS_BUILD_SOFTOKEN_ONLY=1

export NSS_ENABLE_ECC=1

# End -- copied from the build section

# enable the following line to force a test failure
# find . -name \*.chk | xargs rm -f

# Run test suite.

SPACEISBAD=`find ./nss/tests | grep -c ' '` ||:
if [ $SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi

rm -rf ./tests_results
pushd ./nss/tests/
# all.sh is the test suite script

# only run cipher tests for nss-softokn
%global nss_cycles "standard"
%global nss_tests "cipher ec lowhash"
%global nss_ssl_tests " "
%global nss_ssl_run " "

SKIP_NSS_TEST_SUITE=`echo $SKIP_NSS_TEST_SUITE`

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  HOST=localhost DOMSUF=localdomain PORT=$MYRAND NSS_CYCLES=%{?nss_cycles} NSS_TESTS=%{?nss_tests} NSS_SSL_TESTS=%{?nss_ssl_tests} NSS_SSL_RUN=%{?nss_ssl_run} ./all.sh
fi

popd

if [ "x$SKIP_NSS_TEST_SUITE" == "x" ]; then
  TEST_FAILURES=`grep -c FAILED ./tests_results/security/localhost.1/output.log` || :
else
  TEST_FAILURES=0
fi

if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s)"
  exit 1
fi
echo "test suite completed"

%install

%{__rm} -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__mkdir_p} $RPM_BUILD_ROOT/%{saved_files_dir}

# Copy the binary libraries we want
for file in libsoftokn3.so libnssdbm3.so libfreebl3.so libfreeblpriv3.so
do
  %{__install} -p -m 755 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we ship as unsupported
for file in bltest ecperf ectest fipstest shlibsign
do
  %{__install} -p -m 755 dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported_tools_directory}
done

# Copy the include files we want
for file in dist/public/nss/*.h
do
  %{__install} -p -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy some freebl include files we also want
for file in blapi.h alghmac.h
do
  %{__install} -p -m 644 dist/private/nss/$file $RPM_BUILD_ROOT/%{_includedir}/nss3
done

# Copy the static freebl library
for file in libfreebl.a
do
%{__install} -p -m 644 dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the package configuration files
%{__install} -p -m 644 ./dist/pkgconfig/nss-softokn.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss-softokn.pc
%{__install} -p -m 755 ./dist/pkgconfig/nss-softokn-config $RPM_BUILD_ROOT/%{_bindir}/nss-softokn-config


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libnssdbm3.so
%{_libdir}/libsoftokn3.so
# shared with nss-tools
%dir %{_libdir}/nss
%dir %{saved_files_dir}
%dir %{unsupported_tools_directory}
%{unsupported_tools_directory}/bltest
%{unsupported_tools_directory}/ecperf
%{unsupported_tools_directory}/ectest
%{unsupported_tools_directory}/fipstest
%{unsupported_tools_directory}/shlibsign

%files freebl
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license nss/COPYING
%{_libdir}/libfreebl3.so
%{_libdir}/libfreeblpriv3.so

%files freebl-devel
%defattr(-,root,root)
%{_libdir}/libfreebl.a
%{_includedir}/nss3/blapi.h
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/alghmac.h
%{_includedir}/nss3/lowkeyi.h
%{_includedir}/nss3/lowkeyti.h

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/nss-softokn.pc
%{_bindir}/nss-softokn-config

# co-owned with nss
%dir %{_includedir}/nss3
#
# The following headers are those exported public in
# nss/lib/freebl/manifest.mn and
# nss/lib/softoken/manifest.mn
#
# The following list is short because many headers, such as
# the pkcs #11 ones, have been provided by nss-util-devel
# which installed them before us.
#
%{_includedir}/nss3/ecl-exp.h
%{_includedir}/nss3/nsslowhash.h
%{_includedir}/nss3/shsign.h

%changelog
* Thu Dec 29 2016 sulit - 3.27.1-1
- upgrade nss-softokn to 3.27.1

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 3.20.1-2
- Update to 3.20.1

* Fri Oct 23 2015 cjacker - 3.19.2-3
- Rebuild for new 4.0 release

