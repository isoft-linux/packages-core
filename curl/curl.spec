Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name:    curl 
Version: 7.43.0
Release: 2 
License: MIT
Group:   Core/Runtime/Utility 
Source:  http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
URL:     http://curl.haxx.se/

BuildRequires: openssl-devel, libtool, pkgconfig

Requires: libcurl = %{version}-%{release}

%description
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

%package -n libcurl
Group:  Core/Runtime/Library 
Requires: openssl
Summary: Runtime library of libcurl.

%description -n libcurl
Runtime library of libcurl

%package -n libcurl-devel
Group: Core/Development/Library
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

%build
#autoreconf -if
if pkg-config openssl ; then
	CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
	LDFLAGS=`pkg-config --libs openssl`; export LDFLAGS
fi
%configure --with-ssl=%{_prefix} \
    --enable-ipv6 \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
	--without-libidn \
	--enable-static \
    --without-librtmp \
    --without-libssh2 \
    --enable-threaded-resolver \
    --without-libidn \
    --without-libssh2 \
    --without-ssl --with-nss

make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# don't need curl's copy of the certs; use openssl's
find ${RPM_BUILD_ROOT} -name ca-bundle.crt -exec rm -f '{}' \;

rpmclean

%check
#totally 938 checks
make check -n

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
* Wed Oct 15 2014 Cjacker <cjacker@gmail.com>
- review package.
- build for musl linux.

