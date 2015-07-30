%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%global majorver 5.45

Summary: A program-script interaction and testing utility
Name: expect
Version: %{majorver}
Release: 10
License: Public Domain
Group: CoreDev/Runtime/Utility
URL: http://expect.nist.gov/
Source: http://downloads.sourceforge.net/%{name}/%{name}%{version}.tar.gz
Buildrequires: tcl-devel autoconf automake
Patch0: expect-5.43.0-log_file.patch
Patch1: expect-5.43.0-pkgpath.patch
Patch2: expect-5.45-man-page.patch
Patch3: expect-5.45-match-gt-numchars-segfault.patch
Patch100: expect-5.32.2-random.patch
Patch101: expect-5.45-mkpasswd-dash.patch
Patch102: expect-5.45-check-telnet.patch
Patch103: expect-5.45-passmass-su-full-path.patch

%description
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expect and some scripts that use it.

%package devel
Summary: A program-script interaction and testing utility
Group:  CoreDev/Development/Library 
Requires: expect = %{version}-%{release}

%description devel
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains development files for the expect library.

%prep
%setup -q -n expect%{version}
%patch0 -p1 -b .log_file
%patch1 -p1 -b .pkgpath
%patch2 -p1 -b .man-page
%patch3 -p1 -b .match-gt-numchars-segfault
# examples fixes
%patch100 -p1 -b .random
%patch101 -p1 -b .mkpasswd-dash
%patch102 -p1 -b .check-telnet
%patch103 -p1 -b .passmass-su-full-path
# -pkgpath.patch touch configure.in
aclocal
autoconf
( cd testsuite
  autoconf -I.. )

%build
%configure --with-tcl=%{_libdir} --without-tk --enable-shared \
	--with-tclinclude=%{_includedir}/tcl-private/generic
make %{?_smp_mflags}

%check
make test

%install
rm -rf "$RPM_BUILD_ROOT"
make install DESTDIR="$RPM_BUILD_ROOT"

# move
mv "$RPM_BUILD_ROOT"%{tcl_sitearch}/expect%{version}/libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir}

# for linking with -lexpect
ln -s libexpect%{majorver}.so "$RPM_BUILD_ROOT"%{_libdir}/libexpect.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f "$RPM_BUILD_ROOT"%{_bindir}/{cryptdir,decryptdir}
rm -f "$RPM_BUILD_ROOT"%{_mandir}/man1/{cryptdir,decryptdir}.1*
rm -f "$RPM_BUILD_ROOT"%{_bindir}/autopasswd


%clean
rm -rf "$RPM_BUILD_ROOT"


%files
%defattr(-,root,root,-)
%{_bindir}/expect
%{_bindir}/autoexpect
%{_bindir}/dislocate
%{_bindir}/ftp-rfc
%{_bindir}/kibitz
%{_bindir}/lpunlock
%{_bindir}/mkpasswd
%{_bindir}/passmass
%{_bindir}/rftp
%{_bindir}/rlogin-cwd
%{_bindir}/timed-read
%{_bindir}/timed-run
%{_bindir}/unbuffer
%{_bindir}/weather
%{_bindir}/xkibitz
%dir %{tcl_sitearch}/expect%{version}
%{tcl_sitearch}/expect%{version}/pkgIndex.tcl
%{_libdir}/libexpect%{version}.so
%{_libdir}/libexpect.so
%{_mandir}/man1/autoexpect.1.gz
%{_mandir}/man1/dislocate.1.gz
%{_mandir}/man1/expect.1.gz
%{_mandir}/man1/kibitz.1.gz
%{_mandir}/man1/mkpasswd.1.gz
%{_mandir}/man1/passmass.1.gz
%{_mandir}/man1/tknewsbiff.1.gz
%{_mandir}/man1/unbuffer.1.gz
%{_mandir}/man1/xkibitz.1.gz

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/libexpect.3*
%{_includedir}/*

