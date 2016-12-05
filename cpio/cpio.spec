%define _bindir /bin

Summary: A GNU archiving program
Name: cpio
Version: 2.12
Release: 1
License: GPLv3+
URL: http://www.gnu.org/software/cpio/
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2
Source1: cpio.1
Patch1: cpio-2.6-setLocale.patch
Patch2: cpio-2.9-rh.patch
Patch4: cpio-2.9-exitCode.patch
Patch6: cpio-2.9-dev_number.patch
Patch8: cpio-2.9.90-defaultremoteshell.patch
Patch9: cpio-2.10-patternnamesigsegv.patch
Patch10: cpio-2.10-longnames-split.patch
Patch11: cpio-2.11-crc-fips-nit.patch
BuildRequires: autoconf, gettext

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1  -p1 -b .setLocale
%patch2  -p1 -b .rh
%patch4  -p1 -b .exitCode
%patch6  -p1 -b .dev_number
%patch8  -p1 -b .defaultremote
%patch9  -p1 -b .patternnamesigsegv
%patch10  -p1 -b .longnames-split
%patch11  -p1 -b .crc-fips-nit

autoheader

%build
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -Wall" %configure 
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install


rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*.1*
install -c -p -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1

%find_lang %{name}


%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%{_bindir}/*
%{_mandir}/man*/*
%{_libexecdir}/rmt
%changelog
* Mon Dec 05 2016 sulit - 2.12-1
- upgrade cpio to 2.12
- repatch cpio

* Fri Oct 23 2015 cjacker - 2.10-2
- Rebuild for new 4.0 release

