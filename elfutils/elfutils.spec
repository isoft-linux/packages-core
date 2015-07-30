%global _program_prefix eu-

Name:	    elfutils
Version:	0.162
Release:	1
Summary:	ELF related library from elfutils 

Group:		Core/Development/Utility
License:	GPL2
URL:		https://fedorahosted.org/elfutils/
Source0:	https://fedorahosted.org/releases/e/l/elfutils/%{version}/elfutils-%{version}.tar.bz2
Patch0:     https://fedorahosted.org/releases/e/l/elfutils/%{version}/elfutils-portability-%{version}.patch
Patch2:     libelf-build-with-clang.patch 
Patch3:     elfutils-disable-werror.patch
Requires:   libelfutils = %{version}-%{release}
%description
%{summary}


%package -n libelfutils
Summary: Libraries to handle compiled objects
Group:  Core/Runtime/Library 
License: GPLv2+ or LGPLv3+

%description -n libelfutils
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling.  These libraries are used by the programs
in the elfutils package.  The elfutils-devel package enables building
other programs using these libraries.

%package -n libelfutils-devel
Summary: Development files for the libelf library
Group:  Core/Development/Library 
Requires: lib%{name} = %{version}-%{release}

%description -n libelfutils-devel
The header files and libraries of libelf

%prep
%setup -q
%patch0 -p1
#fix inline function clang did not support.
%patch2 -p1
%patch3 -p1

%build
#still can not build with clang, since:
#fields must have a constant size: 'variable length array in structure' extension will never be supported
autoreconf -ivf
%configure --disable-werror
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rpmclean

%check
make check

%post -n libelfutils -p /sbin/ldconfig
%postun -n libelfutils -p /sbin/ldconfig

%files
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-nm
%{_bindir}/eu-objdump
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strings
%{_bindir}/eu-strip
%{_bindir}/eu-ld
%{_bindir}/eu-unstrip
%{_bindir}/eu-make-debug-archive
%{_bindir}/eu-stack

%files -n libelfutils
%{_libdir}/libasm-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw.so.*
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*
%{_libdir}/elfutils/*

%files -n libelfutils-devel
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so


%changelog

