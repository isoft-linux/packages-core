Name:           nettle
Version:        3.1.1 
Release:        2 
Summary:        A low-level cryptographic library

License:        LGPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Source0:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz

BuildRequires:  gmp-devel m4

%package devel
Summary:        Development headers for a low-level cryptographic library
Requires:       %{name} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains the files needed for developing 
applications with nettle.


%prep
%setup -q

%build
%configure --enable-shared
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

rm -rf $RPM_BUILD_ROOT%{_infodir}

chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.6.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.4.*

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/nettle-lfib-stream
%{_bindir}/pkcs1-conv
%{_bindir}/sexp-conv
%{_bindir}/nettle-hash
%{_bindir}/nettle-pbkdf2
%{_libdir}/libnettle.so.*
%{_libdir}/libhogweed.so.*


%files devel
%{_includedir}/nettle
%{_libdir}/libnettle.so
%{_libdir}/libhogweed.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc



%changelog
* Fri Oct 23 2015 cjacker - 3.1.1-2
- Rebuild for new 4.0 release

