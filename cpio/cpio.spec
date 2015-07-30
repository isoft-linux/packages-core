%define _bindir /bin

Summary: A GNU archiving program
Name: cpio
Version: 2.10
Release: 1 
License: GPLv3+
Group: Core/Runtime/Utility
URL: http://www.gnu.org/software/cpio/
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2
Source1: cpio.1
Patch1: cpio-2.6-setLocale.patch
Patch2: cpio-2.9-rh.patch
Patch3: cpio-2.9-chmodRaceC.patch
Patch4: cpio-2.9-exitCode.patch
Patch5: cpio-2.9-dir_perm.patch
Patch6: cpio-2.9-dev_number.patch
Patch7: cpio-2.9-sys_umask.patch
Patch8: cpio-2.9.90-defaultremoteshell.patch
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
%patch3  -p1 -b .chmodRaceC
%patch4  -p1 -b .exitCode
%patch5  -p1 -b .dir_perm
%patch6  -p1 -b .dev_number
%patch7  -p1 -b .sys_umask
%patch8  -p1 -b .defaultremote

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

rpmclean

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
