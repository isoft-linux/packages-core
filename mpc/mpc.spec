Name:           mpc
Version:        1.0.3
Release:        1
Summary:        Library for the arithmetic of complex numbers with arbitrarily high precision
Group:  Core/Runtime/Library	
License:        LGPL
URL:            http://www.multiprecision.org
Source0:        http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz

Requires:       mpfr >= 2.4.1

%description
Library for the arithmetic of complex numbers with arbitrarily high precision


%package        devel
Summary:        Development files for %{name}
Group:	    Core/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n mpc-%{version}


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}
rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so


%changelog
