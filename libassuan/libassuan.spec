Name:    libassuan
Summary: GnuPG IPC library
Version: 2.2.1
Release: 6

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
Source0: ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2
URL:     http://www.gnupg.org/

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages.

%package devel 
Summary: GnuPG IPC library 
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: libassuan%{?_isa} = %{version}-%{release}
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.


%prep
%setup -q


%build
%configure 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

## Unpackaged files
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_libdir}/lib*.la


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/libassuan.so.0*

%files devel 
%defattr(-,root,root,-)
%{_bindir}/libassuan-config
%{_includedir}/*.h
%{_libdir}/libassuan.so
%{_datadir}/aclocal/libassuan.m4


%changelog
* Fri Oct 23 2015 cjacker - 2.2.1-6
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

