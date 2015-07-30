Summary: GNU's bc (a numeric processing language) and dc (a calculator)
Name: bc
Version: 1.06.95
Release: 15%{?dist}
License: GPLv2+
URL: http://www.gnu.org/software/bc/
Group: Applications/Engineering
Source: ftp://alpha.gnu.org/pub/gnu/bc/bc-%{version}.tar.bz2
Patch1: bc-1.06-dc_ibase.patch
Patch2: bc-1.06.95-memleak.patch
Patch3: bc-1.06.95-matlib.patch
Patch4: bc-1.06.95-sigintmasking.patch
Patch5: bc-1.06.95-doc.patch

BuildRequires: readline-devel, flex, bison

%description
The bc package includes bc and dc. Bc is an arbitrary precision
numeric processing arithmetic language. Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%prep
%setup -q
%patch1 -p1 -b .dc_ibase
%patch2 -p1 -b .memleak
%patch3 -p1 -b .matlib
%patch4 -p1 -b .sigintmask
%patch5 -p1 -b .doc

%build
%configure --with-readline
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_infodir}

%check
echo "quit" | ./bc/bc -l Test/checklib.b

%files
%defattr(-,root,root,-)
%{_bindir}/dc
%{_bindir}/bc
%{_mandir}/*/*

%changelog
