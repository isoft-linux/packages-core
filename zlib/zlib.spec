Summary: The compression and decompression library
Name: zlib
Version: 1.2.8
Release: 10%{?dist}
# /contrib/dotzlib/ have Boost license
License: zlib and Boost
URL: http://www.zlib.net/
Source: http://www.zlib.net/zlib-%{version}.tar.xz

Patch0: zlib-1.2.5-minizip-fixuncrypt.patch
# resolves: #805113
Patch1: zlib-1.2.7-optimized-s390.patch
# resolves: #844791
Patch2: zlib-1.2.7-z-block-flush.patch
# resolves: #985344
# http://mail.madler.net/pipermail/zlib-devel_madler.net/2013-August/003081.html
Patch3: zlib-1.2.8-minizip-include.patch

BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%package -n minizip
Summary: Library for manipulation with .zip archives
Requires: %{name} = %{version}-%{release}

%description -n minizip
Minizip is a library for manipulation with files from .zip archives.

%package -n minizip-devel
Summary: Development files for the minizip library
Requires: minizip = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: pkgconfig

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%prep
%setup -q
%patch0 -p1 -b .fixuncrypt
%ifarch s390 s390x
%patch1 -p1 -b .optimized-deflate
%endif
%patch2 -p1 -b .z-flush
%patch3 -p1 -b .minizip_include
iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog.tmp
mv ChangeLog.tmp ChangeLog

%build
%if 0%{?rhel} >= 7
    %ifarch ppc64
        export CFLAGS="$RPM_OPT_FLAGS -O3"
    %else
        export CFLAGS="$RPM_OPT_FLAGS"
    %endif
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif
export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"
./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
make %{?_smp_mflags}

cd contrib/minizip
autoreconf --install
%configure --enable-static=no
make %{?_smp_mflags}

%check
make test

%install
make install DESTDIR=$RPM_BUILD_ROOT

cd contrib/minizip
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license README
%doc ChangeLog FAQ
%{_libdir}/libz.so.*

%files devel
%{!?_licensedir:%global license %%doc}
%license README
%doc doc/algorithm.txt test/example.c
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%{!?_licensedir:%global license %%doc}
%license README
%{_libdir}/libz.a

%files -n minizip
%doc contrib/minizip/MiniZip64_info.txt contrib/minizip/MiniZip64_Changes.txt
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%dir %{_includedir}/minizip
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.2.8-10
- Rebuild for new 4.0 release

