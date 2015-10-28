Name: dosfstools
Summary: Utilities for making and checking MS-DOS FAT filesystems on Linux
Version: 3.0.26
Release: 6
License: GPLv3+
Source0: http://www.daniel-baumann.ch/software/dosfstools/%{name}-%{version}.tar.xz

URL: http://www.daniel-baumann.ch/software/dosfstools/

%description
The dosfstools package includes the mkdosfs and dosfsck utilities,
which respectively make and check MS-DOS FAT filesystems on hard
drives or on floppies.

%prep
%setup -q 

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fno-strict-aliasing" CC=gcc

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-bin install-man PREFIX=%{_prefix} SBINDIR=/sbin

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/sbin/*
%{_mandir}/man8/*

%changelog
* Fri Oct 23 2015 cjacker - 3.0.26-6
- Rebuild for new 4.0 release

