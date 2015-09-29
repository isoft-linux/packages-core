Name: libgcrypt
Version: 1.6.3
Release: 2 
URL: http://www.gnupg.org/
Source0: libgcrypt-%{version}.tar.bz2
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gawk, libgpg-error-devel >= 1.4, pkgconfig
Group:  Core/Runtime/Library 

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Group: Core/Development/Library
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

%prep
%setup -q
%build
%configure --disable-static \
     --enable-noexecstack \

make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/gcrypt

rm -rf $RPM_BUILD_ROOT%{_infodir}

rpmclean

%check
make check

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/gcrypt
%{_libdir}/libgcrypt.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%changelog
