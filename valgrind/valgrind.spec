Summary: Tool for finding memory management bugs in programs
Name: valgrind
Version: 3.11.0
Release: 2
Epoch: 1
Source0: http://valgrind.org/downloads/%{name}-%{version}.tar.bz2

# Needs investigation and pushing upstream
Patch1: valgrind-3.9.0-cachegrind-improvements.patch

# KDE#211352 - helgrind races in helgrind's own mythread_wrapper
Patch2: valgrind-3.9.0-helgrind-race-supp.patch

# Make ld.so supressions slightly less specific.
Patch3: valgrind-3.9.0-ldso-supp.patch

# KDE#353083 arm64 doesn't implement various xattr system calls.
Patch4: valgrind-3.11.0-arm64-xattr.patch

# KDE#353084 arm64 doesn't support sigpending system call.
Patch5: valgrind-3.11.0-arm64-sigpending.patch

# KDE#353370 don't advertise RDRAND in cpuid for Core-i7-4910-like avx2
Patch6: valgrind-3.11.0-no-rdrand.patch

# KDE#278744 cvtps2pd with redundant RexW
Patch7: valgrind-3.11.0-rexw-cvtps2pd.patch

# KDE#353680 Crash with certain glibc versions due to non-implemented TBEGIN
Patch8: valgrind-3.11.0-s390-hwcap.patch

# KDE#355188 valgrind should intercept all malloc related global functions
Patch9: valgrind-3.11.0-wrapmalloc.patch

Patch10: valgrind-disable-some-tests-to-avoid-hang.patch

License: GPLv2
URL: http://www.valgrind.org/

BuildRequires: glibc-devel

BuildRequires: gdb
BuildRequires: binutils
BuildRequires: procps
BuildRequires: perl(Getopt::Long)


# Disable build root strip policy
%define __spec_install_post /usr/lib/rpm/brp-compress || :

# Disable -debuginfo package generation
%define debug_package	%{nil}

%description
Valgrind is a tool to help you find memory-management problems in your
programs. When a program is run under Valgrind's supervision, all
reads and writes of memory are checked, and calls to
malloc/new/free/delete are intercepted. As a result, Valgrind can
detect a lot of problems that are otherwise very hard to
find/diagnose.

%package devel
Summary: Development files for valgrind
Requires: valgrind = %{epoch}:%{version}-%{release}

%description devel
Header files and libraries for development of valgrind aware programs
or valgrind plugins.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

rm -rf gdbserver_tests/mcvabits.*
rm -rf gdbserver_tests/nlcontrolc.*
rm -rf memcheck/tests/descr_belowsp.*
rm -rf ./none/tests/linux/pthread-stack.*

%build
export CC=gcc
export CXX=g++

if [ ! -f "configure" ]; then ./autogen.sh; fi 
%configure
make %{?_smp_mflags}

# Ensure there are no unexpected file descriptors open,
# the testsuite otherwise fails.
cat > close_fds.c <<EOF
#include <stdlib.h>
#include <unistd.h>
int main (int argc, char *const argv[])
{
  int i, j = sysconf (_SC_OPEN_MAX);
  if (j < 0)
    exit (1);
  for (i = 3; i < j; ++i)
    close (i);
  execvp (argv[1], argv + 1);
  exit (1);
}
EOF
gcc $RPM_OPT_FLAGS -o close_fds close_fds.c

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

#do not strip /usr/lib/valgrind/*
#pushd $RPM_BUILD_ROOT/%{_bindir}
#strip --strip-debug * || echo
#popd

%check 
make check ||:
##./close_fds make regtest || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*[^ao]
%{_libdir}/valgrind/[^l]*o
%{_mandir}/man1/*
%{_docdir}/valgrind/*

%files devel
%defattr(-,root,root)
%{_includedir}/valgrind
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*.a
%{_libdir}/pkgconfig/*

%changelog
* Fri Nov 27 2015 Cjacker <cjacker@foxmail.com> - 1:3.11.0-2
- Update

* Fri Oct 23 2015 cjacker - 1:3.10.1-2.svn20150713
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

