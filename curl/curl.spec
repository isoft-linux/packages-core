Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name:    curl 
Version: 7.45.0
Release: 1
License: MIT
Source0:  http://curl.haxx.se/download/%{name}-%{version}.tar.bz2

# use localhost6 instead of ip6-localhost in the curl test-suite
Patch0: 0104-curl-7.19.7-localhost6.patch

# work around valgrind bug (#678518)
Patch1: 0107-curl-7.21.4-libidn-valgrind.patch

URL:     http://curl.haxx.se/

BuildRequires: libtool
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn-devel
BuildRequires: libmetalink-devel
BuildRequires: libnghttp2-devel
BuildRequires: nss-devel
BuildRequires: openldap-devel
BuildRequires: pkgconfig
BuildRequires: python
BuildRequires: zlib-devel

# perl modules used in the test suite
BuildRequires: perl(Cwd)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(strict)
BuildRequires: perl(Time::Local)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(warnings)
BuildRequires: perl(vars)

%ifarch %{ix86} x86_64
BuildRequires: valgrind
%endif

Requires: libcurl = %{version}-%{release}

%description
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

%package -n libcurl
Requires: openssl
Summary: Runtime library of libcurl.

%description -n libcurl
Runtime library of libcurl

%package -n libcurl-devel
Requires: libcurl = %{version}-%{release}
Requires: openssl-devel, pkgconfig
Provides: %{name}-devel = %{version}-%{release}
Summary: Files needed for building applications with libcurl

%description -n libcurl-devel 
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The curl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

# disable test 1112 (#565305) and test 1801
# <https://github.com/bagder/curl/commit/21e82bd6#commitcomment-12226582>
printf "1112\n1801\n" >> tests/data/DISABLED

%build
#autoreconf -if
if pkg-config openssl ; then
  CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
  LDFLAGS=`pkg-config --libs openssl`; export LDFLAGS
fi
%configure --with-ssl=%{_prefix} \
    --enable-ipv6 \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
    --enable-static \
    --without-librtmp \
    --without-libssh2 \
    --enable-threaded-resolver \
    --with-libidn \
    --with-libmetalink \
    --with-nghttp2 \
    --without-libssh2 \
    --without-ssl --with-nss

make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# don't need curl's copy of the certs; use openssl's
find ${RPM_BUILD_ROOT} -name ca-bundle.crt -exec rm -f '{}' \;


%check
#totally 938 checks
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export LD_LIBRARY_PATH

# uncomment to use the non-stripped library in tests
# LD_PRELOAD=`find -name \*.so`
# LD_PRELOAD=`readlink -f $LD_PRELOAD`

cd tests
make %{?_smp_mflags}

./runtests.pl -a -b90 -p -v '!flaky'

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libcurl -p /sbin/ldconfig
%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n libcurl 
%defattr(-,root,root)
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root)
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/libcurl.m4
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 7.43.0-3
- Rebuild for new 4.0 release

* Wed Oct 15 2014 Cjacker <cjacker@gmail.com>
- review package.
- build for musl linux.

