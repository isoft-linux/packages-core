Summary: The GNU data compression program
Name: gzip
Version: 1.8
Release: 1
License: GPLv3+ and GFDL
Source: http://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.xz
URL: http://www.gzip.org/
Conflicts: filesystem < 3
Provides: /bin/gunzip
Provides: /bin/gzip
Provides: /bin/zcat
#for one check
BuildRequires: less, /bin/more

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%prep
%setup -q
%build
export DEFS="NO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
%configure 
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall  bindir=${RPM_BUILD_ROOT}/%{_bindir}

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}%{_infodir}
# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}/%{_bindir}/uncompress

%check
make check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 1.8-1
- update gzip to 1.8
- add more command BuildRequires

* Fri Oct 23 2015 cjacker - 1.6-7
- Rebuild for new 4.0 release

