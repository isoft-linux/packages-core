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

%define main_ver 3.4
%define realname Python
Summary: An interpreted, interactive, object-oriented programming language 
Name:    python3
Version: 3.4.3
Release: 2 
License: BSD
Source0:  %{realname}-%{version}.tar.xz

# Supply various useful macros for building python 3 modules:
#  __python3, python3_sitelib, python3_sitearch
Source2: macros.python3

# Supply an RPM macro "py_byte_compile" for the python3-devel subpackage
# to enable specfiles to selectively byte-compile individual files and paths
# with different Python runtimes as necessary:
Source3: macros.pybytecompile3

#for tkinter
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  tix-devel


BuildRequires: autoconf
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


Provides: /bin/python3
Provides: /bin/python%{main_ver}
Provides: /usr/bin/python%{main_ver}
Provides: /usr/bin/python%{main_ver}m

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

%package devel
Summary: Libraries and header files required for %{name}.
Requires: %{name} = %{version}-%{release}

%description devel
Libraries and header files required for %{name}.

%package tools
Summary: A collection of development tools included with Python
Requires: %{name} = %{version}-%{release}
Requires: tkinter3 = %{version}-%{release}

%description tools
This package includes several tools to help with the development of Python
programs, including IDLE (an IDE with editing and debugging facilities), a
color editor (pynche), and a python gettext program (pygettext.py).

%package -n tkinter3
Summary: A graphical user interface for the Python scripting language
Requires: %{name} = %{version}-%{release}

%description -n tkinter3
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.


%prep
%setup -q -n %{realname}-%{version}

sed -i "s@#! /usr/local/bin/python@#! /usr/bin/env python3@" Lib/cgi.py

%build
%configure --enable-shared --enable-ipv6 --with-system-ffi 
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=%{buildroot}
mv $RPM_BUILD_ROOT/%{_bindir}/2to3 $RPM_BUILD_ROOT/%{_bindir}/2to3-py3

# Install macros for rpm:
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE2} %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE3} %{buildroot}/%{_rpmconfigdir}/macros.d/

#fix permission, it will affect debuginfo package generation.
chmod 0755 %{buildroot}%{_libdir}/libpython3.so
chmod 0755 %{buildroot}%{_libdir}/libpython3*.so.*

%check
#EXTRATESTOPTS="-x test_gdb"
#EXTRATESTOPTS="$EXTRATESTOPTS" make test


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_mandir}/man1/*
%{_libdir}/python*/*
%{_libdir}/*.so.*
%{_bindir}/*

#in devel
%exclude %{_libdir}/python*/config-*/
%exclude %{_bindir}/python*-config

#tkinter
%exclude %{_libdir}/python*/tkinter
%exclude %{_libdir}/python*/lib-dynload/_tkinter*.so

#tools
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files devel
%defattr(-,root,root,-)
%{_includedir}/python*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%{_libdir}/python*/config-*/
%{_bindir}/python*-config

%{_rpmconfigdir}/macros.d/macros.python3
%{_rpmconfigdir}/macros.d/macros.pybytecompile3



%files tools
%defattr(-,root,root,755)
%{_bindir}/2to3*
%{_bindir}/idle*

%files -n tkinter3
%defattr(-,root,root,755)
%{_libdir}/python*/tkinter
%{_libdir}/python*/lib-dynload/_tkinter*.so


%changelog
* Fri Oct 23 2015 cjacker - 3.4.3-2
- Rebuild for new 4.0 release

