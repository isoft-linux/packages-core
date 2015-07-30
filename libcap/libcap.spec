Name: libcap
Version: 2.24
Release: 1 
Summary: Library for getting and setting POSIX.1e capabilities
Source: https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-%{version}.tar.xz

URL: http://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.6/
License: LGPLv2+
Group:  Core/Runtime/Library
BuildRequires: libattr-devel pam-devel

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package devel
Summary: Development files for libcap
Group: Core/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

%prep
%setup -q

%build
# libcap can not be build with _smp_mflags:
make PREFIX=%{_prefix} LIBDIR=%{_lib} SBINDIR=%{_sbindir} \
     INCDIR=%{_includedir} MANDIR=%{_mandir} COPTFLAG="$RPM_OPT_FLAGS"

%install
rm -rf ${RPM_BUILD_ROOT}
make install RAISE_SETFCAP=no \
             DESTDIR=${RPM_BUILD_ROOT} \
             LIBDIR=${RPM_BUILD_ROOT}%{_libdir} \
             SBINDIR=${RPM_BUILD_ROOT}/%{_sbindir} \
             INCDIR=${RPM_BUILD_ROOT}/%{_includedir} \
             MANDIR=${RPM_BUILD_ROOT}/%{_mandir}/ \
             COPTFLAG="$RPM_OPT_FLAGS"
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man{2,3,8}
#mv -f doc/*.2 ${RPM_BUILD_ROOT}/%{_mandir}/man2/
mv -f doc/*.3 ${RPM_BUILD_ROOT}/%{_mandir}/man3/

# remove static lib
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcap.a

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so.*
rpmclean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_libdir}/security/pam_cap.so
%doc doc/capability.notes License

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
