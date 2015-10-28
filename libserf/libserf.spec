%define real_name serf

Summary: HTTP client library written in C using apr
Name: libserf
Version: 1.3.5 
Release: 2
License: Apache License 2.0
URL: http://code.google.com/p/serf/

Source: http://serf.googlecode.com/files/serf-%{version}.tar.bz2
Source1:scons-local-2.3.0.tar.gz
 
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: openssl-devel
Requires: apr
Requires: apr-util
Requires: openssl

%description
HTTP client library written in C using apr.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -n %{real_name}-%{version} -a1

%build
python scons.py PREFIX=/usr

%install
%{__rm} -rf %{buildroot}
python scons.py install --install-sandbox=%{buildroot}

rm -rf %{buildroot}/%{_libdir}/*.a
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc README
%{_libdir}/libserf*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.3.5-2
- Rebuild for new 4.0 release

