Summary: SPICE protocol headers 
Name: spice-protocol
Version: 0.12.7
Release: 1
License: LGPLv2+
Url:    http://www.spice-space.org
Source: http://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2

%description
SPICE protocol headers

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
%dir %{_includedir}/spice-1
%{_includedir}/spice-1/*
%{_datadir}/pkgconfig/spice-protocol.pc

%changelog
* Sun Aug 09 2015 Cjacker <cjacker@foxmail.com>
- rebuild
