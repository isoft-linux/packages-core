Summary: A GNU file archiving program
Name: tar
Epoch: 2
Version: 1.28
Release: 2
License: GPLv3+
URL: http://www.gnu.org/software/tar/
Source0: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.xz
BuildRequires: autoconf automake gzip gettext libacl-devel gawk

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package.

%prep
%setup -q

%build
export FORCE_UNSAFE_CONFIGURE=1 
%configure 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/%{_infodir}

# XXX Nuke unpackaged files.
rm -f ${RPM_BUILD_ROOT}%{_sbindir}/rmt


%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man1/tar.1.gz
%changelog
* Fri Oct 23 2015 cjacker - 2:1.28-2
- Rebuild for new 4.0 release

