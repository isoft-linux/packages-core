Summary: The GNU macro processor
Name:    m4
Version: 1.4.17
Release: 2
License: GPL
Source0: ftp://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz
Patch1: m4-no-overflow-under-clang.patch

URL: http://www.gnu.org/software/m4/

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -q
%patch1 -p1

%build
autoreconf -ivf
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
make check

%files
%defattr(-,root,root)
%{_bindir}/m4
%{_mandir}/man1/m4.1*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 23 2015 cjacker - 1.4.17-2
- Rebuild for new 4.0 release

