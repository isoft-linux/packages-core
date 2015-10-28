Summary: CMS and X.509 library
Name:    libksba
Version: 1.3.3
Release: 4

# The library is licensed under LGPLv3+ or GPLv2+,
# the rest of the package under GPLv3+
License: (LGPLv3+ or GPLv2+) and GPLv3+
URL:     http://www.gnupg.org/
Source0: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: libgcrypt-devel >= 1.2.0

%description
KSBA (pronounced Kasbah) is a library to make X.509 certificates as
well as the CMS easily accessible by other applications.  Both
specifications are building blocks of S/MIME and TLS.

%package devel
Summary: Development headers and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

%build
%configure \
  --disable-dependency-tracking \
  --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libksba.so.8*

%files devel
%defattr(-,root,root,-)
%{_bindir}/ksba-config
%{_libdir}/libksba.so
%{_includedir}/ksba.h
%{_datadir}/aclocal/ksba.m4


%changelog
* Fri Oct 23 2015 cjacker - 1.3.3-4
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

