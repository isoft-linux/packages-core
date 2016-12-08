Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.6.2
Release: 1
License: BSD
URL: http://flex.sourceforge.net/
Source: flex-%{version}.tar.gz
# cxx_restart test fail, it's a bug
# https://github.com/westes/flex/issues/98
Patch0: flex-do-not-enable-cxx_restart-test.patch

Requires: m4
BuildRequires: gettext bison m4 help2man

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

%package        devel
Summary:        This package contains the static library and headers for flex.

%description    devel
This package contains the static library for flex.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-dependency-tracking --disable-shared CFLAGS="-fPIC $RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_infodir}

( cd ${RPM_BUILD_ROOT}
  ln -sf flex .%{_bindir}/lex
  ln -sf flex .%{_bindir}/flex++
  ln -s flex.1 .%{_mandir}/man1/lex.1
  ln -s flex.1 .%{_mandir}/man1/flex++.1
  ln -s libfl.a .%{_libdir}/libl.a
)

%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/*
#%{_libdir}/libfl.so.*
#%{_libdir}/libfl_pic.so.*
%{_mandir}/man1/*
%{_datadir}/locale/*
%{_datadir}/doc/flex/*

%files devel 
%defattr(-,root,root)
#%{_libdir}/libfl.so
#%{_libdir}/libfl_pic.so
%{_libdir}/*.a
%{_includedir}/FlexLexer.h
%changelog
* Thu Dec 08 2016 sulit - 2.6.2-1
- upgrade flex to 2.6.2

* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 2.6.0-1
- update flex to 2.6.0

* Fri Oct 23 2015 cjacker - 2.5.39-8
- Rebuild for new 4.0 release

