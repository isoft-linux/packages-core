Summary: A GNU general-purpose parser generator
Name: bison
Version: 3.0.2 
Release: 4
License: GPLv2+
Group:  CoreDev/Development/Utility 
Source: ftp://ftp.gnu.org/pub/gnu/bison/bison-%{version}.tar.xz
URL: http://www.gnu.org/software/bison/
BuildRequires: m4 >= 1.4 
Requires: m4 >= 1.4
BuildRequires: byacc, flex

%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you shouldn't have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

If your system will be used for C development, you should install
Bison.

%package devel
Summary: -ly library for development using Bison-generated parsers
Group: CoreDev/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel
The bison-devel package contains the -ly library sometimes used by
programs using Bison-generated parsers.  If you are developing programs
using Bison, you might want to link with this library.  This library
is not required by all Bison-generated parsers, but may be employed by
simple programs to supply minimal support for the generated parsers.

%prep
%setup -q

%build

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# Remove unpackaged files.
rm -f $RPM_BUILD_ROOT/%{_bindir}/yacc
rm -rf $RPM_BUILD_ROOT/%{_infodir}
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/yacc*

%check
make check

%files
%defattr(-,root,root)
%{_mandir}/*/bison*
%{_datadir}/bison
%{_bindir}/bison
%{_datadir}/aclocal/bison*.m4
%{_datadir}/locale/*

%files devel
%defattr(-,root,root)
%{_libdir}/liby.a

%clean
rm -rf $RPM_BUILD_ROOT

