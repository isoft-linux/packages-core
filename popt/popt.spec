Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:   	1	
License:	MIT
Group:		Core/Runtime/Library
URL:		http://www.rpm5.org/
Source:		http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	gettext

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package devel
Summary:	Development files for the popt library
Group:		Core/Development/Library
Requires:	%{name} = %{version}-%{release}

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%package static
Summary:	Static library for parsing command line parameters
Group:		Core/Development/Library
Requires:	%{name}-devel = %{version}-%{release}

%description static
The popt-static package includes static libraries of the popt library.
Install it if you need to link statically with libpopt.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d

%find_lang popt
rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig 

%files -f popt.lang
%defattr(-,root,root)
%{_sysconfdir}/popt.d
%{_libdir}/libpopt.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libpopt.so
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%{_libdir}/libpopt.a

%changelog
