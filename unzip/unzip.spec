Summary: A utility for unpacking zip files.
Name: unzip
Version: 5.52
release: 8
License: BSD
Group:  Core/Runtime/Utility
Source: ftp://ftp.info-zip.org/pub/infozip/src/unzip552.tgz
Patch0: unzip542-rpmoptflags.patch
Patch1: unzip-chinese.patch
Patch2: unzip-5.50.utf8.patch	
Patch3: unzip-detect-charset.patch
URL: http://www.info-zip.org/pub/infozip/UnZip.html
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The unzip utility is used to list, test, or extract files from a zip
archive.  Zip archives are commonly found on MS-DOS systems.  The zip
utility, included in the zip package, creates zip archives.  Zip and
unzip are both compatible with archives created by PKWARE(R)'s PKZIP
for MS-DOS, but the programs' options and default behaviors do differ
in some respects.

Install the unzip package if you need to list, test or extract files from
a zip archive.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

ln -s unix/Makefile Makefile

%build
make linux_noasm LF2="" 

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr MANDIR=$RPM_BUILD_ROOT/%{_mandir}/man1 install LF2=""

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
