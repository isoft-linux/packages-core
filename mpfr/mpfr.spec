Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 3.1.3
Release: 3 
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
License: LGPL 

BuildRequires: autoconf libtool gmp-devel
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary: Development tools A C library for mpfr library
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel

%description devel
The static libraries, header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q
%build
%configure --disable-assert --enable-shared
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


rm -rf $RPM_BUILD_ROOT%{_libdir}/libmpfr.a
rm -rf $RPM_BUILD_ROOT/%{_docdir}
rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libmpfr.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmpfr.so
%{_includedir}/*.h

%changelog
* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 3.1.3-3
- Add gmp-devel requires to mpfr-devel package

* Fri Oct 23 2015 cjacker - 3.1.3-2
- Rebuild for new 4.0 release


* Thu Sep 03 2015 Cjacker <cjacker@foxmail.com>
- update to 3.1.3
