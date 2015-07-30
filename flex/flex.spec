Summary: A tool for creating scanners (text pattern recognizers)
Name: flex
Version: 2.5.39
Release: 7
License: BSD
Group:  CoreDev/Development/Utility 
URL: http://flex.sourceforge.net/
Source: flex-%{version}.tar.bz2
Patch0: 0001-bison-test-fixes-Do-not-use-obsolete-bison-construct.patch

Requires: m4
BuildRequires: gettext bison m4

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
Group:          CoreDev/Development/Library

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

%files devel 
%defattr(-,root,root)
#%{_libdir}/libfl.so
#%{_libdir}/libfl_pic.so
%{_libdir}/*.a
%{_includedir}/FlexLexer.h
%changelog
