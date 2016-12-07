Summary: A front end for testing other programs
Name: dejagnu
Version: 1.6
Release: 1
Epoch: 1
License: GPLv3+
Source: ftp://ftp.gnu.org/gnu/dejagnu/dejagnu-%{version}.tar.gz
URL: http://www.gnu.org/software/dejagnu/
Requires: expect
BuildArch: noarch
BuildRequires: expect
Patch1: dejagnu-1.5-smp-1.patch
Patch2: dejagnu-1.5-runtest.patch
Patch3: dejagnu-1.5-usrmove.patch
Patch4: dejagnu-1.5-gfortran.patch
Patch5: dejagnu-1.5-aarch64.patch
Patch10: dejagnu-1.5.1-disable-doc.patch

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%patch10 -p1

%build
autoreconf -ivf
%configure -v

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
chmod a-x $RPM_BUILD_ROOT/%{_datadir}/dejagnu/runtest.exp
make DESTDIR=$RPM_BUILD_ROOT install-man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/runtest
%{_datadir}/dejagnu
%{_includedir}/dejagnu.h

%changelog
* Wed Dec 07 2016 sulit - 1:1.6-1
- upgrade dejagnu to 1.6

* Fri Oct 23 2015 cjacker - 1:1.5.1-4
- Rebuild for new 4.0 release

