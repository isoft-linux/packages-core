%define vermajor 1
%define verminor 5.9
%define version %{vermajor}.%{verminor}
%define libapivermajor 1
%define libapiversion %{libapivermajor}.5

# % define buildid .local

Summary: Linux Key Management Utilities
Name: keyutils
Version: %{version}
Release: 6%{?buildid}%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
ExclusiveOS: Linux
Url: http://people.redhat.com/~dhowells/keyutils/

Source0: http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2

BuildRequires: glibc-devel
Requires: keyutils-libs == %{version}-%{release}

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package libs
Summary: Key utilities library
Group: System Environment/Base

%description libs
This package provides a wrapper library for the key management facility system
calls.

%package libs-devel
Summary: Development package for building Linux key management utilities
Group: System Environment/Base
Requires: keyutils-libs == %{version}-%{release}

%description libs-devel
This package provides headers and libraries for building key utilities.

%prep
%setup -q

%define datadir %{_datarootdir}/keyutils

%build
make \
	NO_ARLIB=1 \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{datadir} \
	RELEASE=.%{release} \
	NO_GLIBC_KEYERR=1 \
	CFLAGS="-Wall $RPM_OPT_FLAGS -Werror"

%install
rm -rf $RPM_BUILD_ROOT
make \
	NO_ARLIB=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{datadir} \
	install

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{!?_licensedir:%global license %%doc}
%license LICENCE.GPL
%{_sbindir}/*
%{_bindir}/*
%{datadir}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/*

%files libs
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENCE.LGPL
%{_mandir}/man7/*
%{_libdir}/libkeyutils.so.%{libapiversion}
%{_libdir}/libkeyutils.so.%{libapivermajor}

%files libs-devel
%defattr(-,root,root,-)
%{_libdir}/libkeyutils.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
