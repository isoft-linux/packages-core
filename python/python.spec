# Some of the files below /usr/lib/pythonMAJOR.MINOR/test  (e.g. bad_coding.py)
# are deliberately invalid, leading to SyntaxError exceptions if they get
# byte-compiled.
#
# These errors are ignored by the normal python build, and aren't normally a
# problem in the buildroots since /usr/bin/python isn't present.
#
# However, for the case where we're rebuilding the python srpm on a machine
# that does have python installed we need to set this to avoid
# brp-python-bytecompile treating these as fatal errors:
#
%global _python_bytecompile_errors_terminate_build 0

Name:		python
Version:	2.7.10
Release:	2
Summary:    An interpreted, interactive, object-oriented programming language	

License:	Python
URL:		http://www.python.org
Source0:	Python-%{version}.tar.xz

Source9:  macros.python
Source10:   macros.python2

Patch30:    00153-fix-test_gdb-noise.patch  
Patch31:    00156-gdb-autoload-safepath.patch       
Patch32:    00166-fix-fake-repr-in-gdb-hooks.patch  
Patch33:    00167-disable-stack-navigation-tests-when-optimized-in-test_gdb.patch
Patch34:    00189-gdb-py-bt-dont-raise-exception-from-eval.patch


Provides:   python2 = %{version}-%{release}

#for tkinter
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  tix-devel


BuildRequires: autoconf
BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel

BuildRequires: expat-devel >= 2.1.0

BuildRequires: findutils
BuildRequires: gcc
BuildRequires: gdbm-devel
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: zlib-devel

Requires:	openssl

#these is many automatically genereated files in other package use the first found path.
#since in our os, /bin is a link to /usr/bin(merge /bin /usr/bin).
#so will get the wrong requires of rpm.
Provides: /bin/python

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface.

%package devel
Summary: The libraries and header files needed for Python development
Provides:   python2-devel = %{version}-%{release}
Requires: python = %{version}-%{release}
Requires: pkgconfig

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.


%package tools
Summary: A collection of development tools included with Python
Requires: %{name} = %{version}-%{release}
Requires: tkinter = %{version}-%{release}
Provides: python2-tools = %{version}

%description tools
This package includes several tools to help with the development of Python
programs, including IDLE (an IDE with editing and debugging facilities), a
color editor (pynche), and a python gettext program (pygettext.py).

%package -n tkinter
Summary: A graphical user interface for the Python scripting language
Requires: %{name} = %{version}-%{release}
Provides: tkinter2 = %{version}

%description -n tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%prep
%setup -q -n Python-%{version}
%patch30 -p0
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1

sed -i 's@#! /usr/local/bin/python@#!/usr/bin/env python@g' Lib/cgi.py 

%build
%configure  \
        --enable-shared \
        --with-threads \
        --enable-ipv6 \
        --with-system-ffi \
        --with-system-expat \
        --with-system-zlib \
        --enable-unicode=ucs4

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

# Install macros for rpm:
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE9} %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE10} %{buildroot}/%{_rpmconfigdir}/macros.d/



%check
#skip test_gdb, we do not have debug build.
EXTRATESTOPTS="-x test_gdb"
EXTRATESTOPTS="$EXTRATESTOPTS" make test

%files
%{_bindir}/*
%{_libdir}/libpython2.7.so.1.0
%dir %{_libdir}/python2.7
%{_libdir}/python2.7/*
%{_mandir}/man1/*
#in devel
%exclude %{_libdir}/python2.7/config
%exclude %{_bindir}/python*-config

#tkinter
%exclude %{_libdir}/python2.7/lib-tk
%exclude %{_libdir}/python2.7/lib-dynload/_tkinter.so

#tools
%exclude %{_bindir}/smtpd*.py*
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python2.7/config/*
%{_includedir}/python2.7/*
%{_bindir}/python*-config
%{_libdir}/libpython*.so

%{_rpmconfigdir}/macros.d/macros.python
%{_rpmconfigdir}/macros.d/macros.python2

%files tools
%defattr(-,root,root,755)
%{_bindir}/smtpd*.py*
%{_bindir}/2to3*
%{_bindir}/idle*

%files -n tkinter
%defattr(-,root,root,755)
%{_libdir}/python2.7/lib-tk
%{_libdir}/python2.7/lib-dynload/_tkinter.so


%changelog
* Fri Oct 23 2015 cjacker - 2.7.10-2
- Rebuild for new 4.0 release

