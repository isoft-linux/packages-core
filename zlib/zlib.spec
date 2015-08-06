Summary: The compression and decompression library
Name: zlib
Version: 1.2.8
Release: 2
License: zlib and Boost
Group:   Core/Runtime/Library
URL:    http://www.zlib.net/
Source: http://www.zlib.net/zlib-%{version}.tar.gz

Patch0: zlib-1.2.5-minizip-fixuncrypt.patch
Patch2: zlib-1.2.7-z-block-flush.patch

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Group:   Core/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Group:  Core/Development/Library
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%prep
%setup -q
%patch0 -p1 -b .fixuncrypt
%patch2 -p1 -b .z-flush

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS -Wl,-z,relro"

./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
make %{?_smp_mflags}

%check
make test

%install
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%post 
/sbin/ldconfig /usr/lib/

%postun 
/sbin/ldconfig /usr/lib

%files
%{_libdir}/libz.so.*

%files devel
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_mandir}/man3/zlib.3*

%files static
%{_libdir}/libz.a

%changelog
