Name:		ocl-icd
Version:	2.2.7
Release:	2
Summary:	OpenCL ICD Bindings

License:	BSD
URL:		https://forge.imag.fr/projects/ocl-icd/
Source0:    https://forge.imag.fr/frs/download.php/664/%{name}-%{version}.tar.gz

BuildRequires:	libtool
BuildRequires:	opencl-headers
BuildRequires:	ruby

Provides:	opencl-icd-loader


%description
OpenCL ICD Bindings


%package devel
Summary:	Development files for OpenCL ICD Bindings
Requires:	%{name}%{?_isa} = %{version}-%{release}


%description devel
This package contains the development files for %{name}.


%prep
%setup -q


%build
autoreconf -fiv
%configure
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -type f -name '*.la' -print0 | xargs -0 rm -rf
rm -rf %{buildroot}/%{_defaultdocdir}


%check
make check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc COPYING NEWS README
%{_libdir}/libOpenCL.so.*


%files devel
%doc ocl_icd_loader_gen.map ocl_icd_bindings.c
%{_includedir}/*
%{_libdir}/libOpenCL.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Oct 23 2015 cjacker - 2.2.7-2
- Rebuild for new 4.0 release

