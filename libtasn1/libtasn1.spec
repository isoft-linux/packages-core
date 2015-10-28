Summary:	The ASN.1 library used in GNUTLS
Name:		libtasn1
Version:    4.5
Release:	2

# The libtasn1 library is LGPLv2+, utilities are GPLv3+
License:	GPLv3+ and LGPLv2+
URL:		http://www.gnu.org/software/libtasn1/
Source0:	http://ftp.gnu.org/gnu/libtasn1/%name-%version.tar.gz
Patch1:		libtasn1-2.12-rpath.patch
BuildRequires:	bison, pkgconfig
Provides: bundled(gnulib) = 20120913

%description
A library that provides Abstract Syntax Notation One (ASN.1, as specified
by the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

%package devel
Summary:	Files for development of applications which will use libtasn1
Requires:	%name = %version-%release
Requires:	pkgconfig

%description devel
This package contains files for development of applications which will
use libtasn1.


%package tools
Summary:	Some ASN.1 tools
License:	GPLv3+
Requires:	%name = %version-%release

%description tools
This package contains simple tools that can decode and encode ASN.1
data.


%prep
%setup -q

%patch1 -p1 -b .rpath

%build
%configure --disable-static --disable-silent-rules

make %{?_smp_mflags}


%install
make DESTDIR="$RPM_BUILD_ROOT" install

rm -rf $RPM_BUILD_ROOT%{_infodir}


%check
make check


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc doc/TODO doc/*.pdf
%doc AUTHORS COPYING* NEWS README THANKS
%_libdir/*.so.6*

%files tools
%defattr(-,root,root,-)
%_bindir/asn1*
%_mandir/man1/asn1*

%files devel
%defattr(-,root,root,-)
%_libdir/*.so
%_libdir/pkgconfig/*.pc
%_includedir/*
%_mandir/man3/*asn1*


%changelog
* Fri Oct 23 2015 cjacker - 4.5-2
- Rebuild for new 4.0 release

