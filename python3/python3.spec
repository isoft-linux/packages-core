%global _python_bytecompile_errors_terminate_build 0


# We want to byte-compile the .py files within the packages using the new
# python3 binary.
# 
# Unfortunately, rpmbuild's infrastructure requires us to jump through some
# hoops to avoid byte-compiling with the system python 2 version:
#   /usr/lib/rpm/isoft/macros sets up build policy that (amongst other things)
# defines __os_install_post.  In particular, "brp-python-bytecompile" is
# invoked without an argument thus using the wrong version of python
# (/usr/bin/python, rather than the freshly built python), thus leading to
# numerous syntax errors, and incorrect magic numbers in the .pyc files.  We
# thus override __os_install_post to avoid invoking this script:
%global __os_install_post /usr/lib/rpm/brp-compress \
  %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \
  /usr/lib/rpm/brp-strip-static-archive %{__strip} \
  /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} \
  /usr/lib/rpm/brp-python-hardlink 


%define main_ver 3.5
%global pybasever %{main_ver} 
%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload


%define realname Python

Summary: An interpreted, interactive, object-oriented programming language 
Name:    python3
Version: 3.5.0
Release: 4 
License: BSD
Source0:  %{realname}-%{version}.tar.xz

# Supply various useful macros for building python 3 modules:
#  __python3, python3_sitelib, python3_sitearch
Source2: macros.python3

# Supply an RPM macro "py_byte_compile" for the python3-devel subpackage
# to enable specfiles to selectively byte-compile individual files and paths
# with different Python runtimes as necessary:
Source3: macros.pybytecompile3

# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Was Patch0 in ivazquez' python3000 specfile:
Patch1:         Python-3.1.1-rpath.patch

# 00173 #
# Workaround for ENOPROTOOPT seen in Koji withi test.support.bind_port()
# (rhbz#913732)
Patch173: 00173-workaround-ENOPROTOOPT-in-bind_port.patch


# 00178 #
# Don't duplicate various FLAGS in sysconfig values
# http://bugs.python.org/issue17679
# Does not affect python2 AFAICS (different sysconfig values initialization)
Patch178: 00178-dont-duplicate-flags-in-sysconfig.patch


# Reported upstream in http://bugs.python.org/issue17737
# This patch basically looks at every frame and if it is somehow corrupted,
# it just stops printing the traceback - it doesn't fix the actual bug.
# This bug seems to only affect ARM.
# Doesn't seem to affect Python 2 AFAICS.
Patch179: 00179-dont-raise-error-on-gdb-corrupted-frames-in-backtrace.patch

# Previously, this fixed a problem where some *.py files were not being
# bytecompiled properly during build. This was result of py_compile.compile
# raising exception when trying to convert test file with bad encoding, and
# thus not continuing bytecompilation for other files.
# This was fixed upstream, but the test hasn't been merged yet, so we keep it
Patch186: 00186-dont-raise-from-py_compile.patch

# Tests requiring SIGHUP to work don't work in Koji
Patch194: temporarily-disable-tests-requiring-SIGHUP.patch

# test_threading fails in koji dues to it's handling of signals
Patch203: 00203-disable-threading-test-koji.patch

#for tkinter
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  tix-devel


BuildRequires: autoconf
BuildRequires: bluez-libs-devel

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
BuildRequires: tar
BuildRequires: valgrind-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: net-tools

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
%patch1 -p1
%patch173 -p1
%patch178 -p1
%patch179 -p1
%patch186 -p1
%patch194 -p1
%patch203 -p1

sed -i "s@#! /usr/local/bin/python@#! /usr/bin/env python3@" Lib/cgi.py

%build
%configure --enable-shared --enable-ipv6 --with-system-ffi 
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=%{buildroot}
mv $RPM_BUILD_ROOT/%{_bindir}/2to3 $RPM_BUILD_ROOT/%{_bindir}/2to3-py3

# Development tools
install -m755 -d ${RPM_BUILD_ROOT}%{pylibdir}/Tools
install Tools/README ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/freeze ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/i18n ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/pynche ${RPM_BUILD_ROOT}%{pylibdir}/Tools/
cp -ar Tools/scripts ${RPM_BUILD_ROOT}%{pylibdir}/Tools/

# Documentation tools
install -m755 -d %{buildroot}%{pylibdir}/Doc
cp -ar Doc/tools %{buildroot}%{pylibdir}/Doc/

# Demo scripts
cp -ar Tools/demo %{buildroot}%{pylibdir}/Tools/


# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# .xpm and .xbm files should not be executable:
find %{buildroot} \
  \( -name \*.xbm -o -name \*.xpm -o -name \*.xpm.1 \) \
  -exec chmod a-x {} \;


# Remove executable flag from files that shouldn't have it:
chmod a-x \
  %{buildroot}%{pylibdir}/distutils/tests/Setup.sample \
  %{buildroot}%{pylibdir}/Tools/README

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;

# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;


# Do bytecompilation with the newly installed interpreter.
# This is similar to the script in macros.pybytecompile
# compile *.pyo
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2]) for f in sys.argv[1:]]' || :
# compile *.pyc
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2], optimize=0) for f in sys.argv[1:]]' || :

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} \
    -perm 555 -exec chmod 755 {} \;


# Install macros for rpm:
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE2} %{buildroot}/%{_rpmconfigdir}/macros.d/
install -m 644 %{SOURCE3} %{buildroot}/%{_rpmconfigdir}/macros.d/


# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so (bug 539917)
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)


%check
#test gdb failed.
#test distutils failed with rpmbuild command, it's ok.
EXTRATESTOPTS="-x test_gdb test_distutils"
EXTRATESTOPTS="$EXTRATESTOPTS" make test


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
%exclude %{pylibdir}/Tools
%exclude %{pylibdir}/Doc

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
%{pylibdir}/Tools
%doc %{pylibdir}/Doc

%files -n tkinter3
%defattr(-,root,root,755)
%{_libdir}/python*/tkinter
%{_libdir}/python*/lib-dynload/_tkinter*.so


%changelog
* Mon Nov 23 2015 Cjacker <cjacker@foxmail.com> - 3.5.0-4
- Rebuild

* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 3.5.0-3
- Rebuild

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 3.5.0-2
- Initial build

