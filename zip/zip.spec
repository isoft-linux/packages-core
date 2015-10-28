Summary: A file compression and packaging utility compatible with PKZIP
Name: zip
Version: 3.0
Release: 9 
License: BSD
Source: http://downloads.sourceforge.net/infozip/zip30.tar.gz
URL: http://www.info-zip.org/Zip.html
Patch1: zip-3.0-exec-shield.patch
Patch2: zip-3.0-currdir.patch
Patch3: zip-3.0-time.patch

BuildRequires: bzip2-devel

%description
The zip program is a compression and file packaging utility.  Zip is
analogous to a combination of the UNIX tar and compress commands and
is compatible with PKZIP (a compression and file packaging utility for
MS-DOS systems).

Install the zip package if you need to compress files using the zip
program.

%prep
%setup -q -n zip30
%patch1 -p1 -b .exec-shield
%patch2 -p1 -b .currdir
%patch3 -p1 -b .time

%build
make -f unix/Makefile prefix=%{_prefix} "CFLAGS_NOOPT=-I. -DUNIX $RPM_OPT_FLAGS" generic CC=gcc %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BULD_ROOT%{_mandir}/man1

make -f unix/Makefile prefix=$RPM_BUILD_ROOT%{_prefix} \
        MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install

%files
%defattr(-,root,root,-)
%{_bindir}/zipnote
%{_bindir}/zipsplit
%{_bindir}/zip
%{_bindir}/zipcloak
%{_mandir}/man1/zip.1*
%{_mandir}/man1/zipcloak.1*
%{_mandir}/man1/zipnote.1*
%{_mandir}/man1/zipsplit.1*

%changelog
* Fri Oct 23 2015 cjacker - 3.0-9
- Rebuild for new 4.0 release

