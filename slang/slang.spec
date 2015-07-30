Summary: The shared library for the S-Lang extension language.
Name: slang
Version: 2.2.4
Release: 1 
License: GPL
Group:  Core/Runtime/Library
Source: ftp://ftp.fu-berlin.de/pub/unix/misc/slang/v2.0/slang-%{version}.tar.bz2
Patch0: slang-2.2.3-slsh-libs.patch 
Patch1: musl-fix-posix_close-clash.patch
Url: http://www.s-lang.org/

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package devel
Summary: The static library and header files for development using S-Lang.
Group: Core/Development/Library
Requires: slang = %{version}

%description devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%prep
%setup -n slang-%{version} -q
%patch0 -p1
#%patch1 -p1

%build
%configure --includedir=%{_includedir}/slang
make

%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=${RPM_BUILD_ROOT} install
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so.*
%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libslang*.so.*
%dir %{_libdir}/slang
%{_libdir}/slang/v2/modules/*.so
%{_sysconfdir}/slsh.rc
%{_bindir}/slsh
%{_mandir}/man1/slsh.1*
%dir %{_datadir}/slsh
%{_datadir}/slsh/*

%files devel
%defattr(-,root,root)
#%{_libdir}/libslang*.a
%{_libdir}/libslang*.so
%{_libdir}/pkgconfig/slang.pc
%{_includedir}/slang

%changelog
