Name: dosfstools
Summary: Utilities for making and checking MS-DOS FAT filesystems on Linux
Version: 3.0.28
Release: 7
License: GPLv3+
Source0: https://github.com/dosfstools/dosfstools/releases/download/v%{version}/dosfstools-%{version}.tar.xz

URL: https://github.com/dosfstools/dosfstools

%description
The dosfstools package includes the mkdosfs and dosfsck utilities,
which respectively make and check MS-DOS FAT filesystems on hard
drives or on floppies.

%prep
%setup -q 

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-bin install-man install-symlinks PREFIX=%{_prefix}

rm -rf %{buildroot}%{_mandir}/de
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 3.0.28-7
- Update to 3.0.28, fix mkfs.vfat missing

* Fri Oct 23 2015 cjacker - 3.0.26-6
- Rebuild for new 4.0 release

