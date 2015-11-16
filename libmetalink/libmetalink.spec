Name:		libmetalink
Version:	0.1.3
Release:	2%{?dist}
Summary:	Metalink library written in C
License:	MIT
URL:		https://launchpad.net/libmetalink
Source0:	http://launchpad.net/libmetalink/trunk/packagingfix/+download/%{name}-%{version}.tar.xz
BuildRequires:	expat-devel
BuildRequires:	CUnit-devel

%description
libmetalink is a Metalink C library. It adds Metalink functionality such as
parsing Metalink XML files to programs written in C.

%package	devel
Summary:	Files needed for developing with %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Files needed for building applications with libmetalink.

%prep
%setup -q

%build
#fix build warnings
export CFLAGS="-D_DEFAULT_SOURCE"
%configure --disable-static
make %{?_smp_mflags}

%check
#without CUnit, make check will be skiped.
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name *.la -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README 
%{_libdir}/libmetalink.so.*


%files devel
%dir %{_includedir}/metalink/
%{_includedir}/metalink/metalink_error.h
%{_includedir}/metalink/metalink.h
%{_includedir}/metalink/metalink_parser.h
%{_includedir}/metalink/metalink_types.h
%{_includedir}/metalink/metalinkver.h
%{_libdir}/libmetalink.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*


%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 0.1.3-2
- Initial build

