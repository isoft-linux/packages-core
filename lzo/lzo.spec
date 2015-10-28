Name:           lzo
Version:        2.09
Release:        4 
Summary:        Data compression library with very fast (de)compression
License:        GPL
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package devel
Summary:        Development files for the lzo library
Requires:       %{name} = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.


%prep
%setup -q

for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/liblzo2.la
#no need to ship
rm -rf $RPM_BUILD_ROOT%{_docdir}/lzo


%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING THANKS NEWS
%{_libdir}/liblzo2.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/liblzo2.so


%changelog
* Fri Oct 23 2015 cjacker - 2.09-4
- Rebuild for new 4.0 release

