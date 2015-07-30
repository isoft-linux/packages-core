Summary: A GNU arbitrary precision library
Name: gmp
Version: 6.0.0 
Release: 3
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}a.tar.xz
License: LGPL 
Group:  Core/Runtime/Library 

BuildRequires: m4
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package devel
Summary: Development tools for the GNU MP arbitrary precision library
Group: Core/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel
The static libraries, header files and documentation for using the GNU
MP arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%prep
%setup -q 

%build
if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="gcc -c -Wa,--noexecstack"
fi

mkdir base
cd base
ln -s ../configure .
%configure
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
cd ..

%check
%ifnarch ppc
cd base
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check
cd ..
%endif



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libgmp.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/*.h

%changelog
