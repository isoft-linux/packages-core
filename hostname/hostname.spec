Summary: Utility to set/show the host name or domain name
Name: hostname
Version: 3.15
Release: 5
License: GPLv2+
URL: http://packages.qa.debian.org/h/hostname.html
Source0: http://ftp.de.debian.org/debian/pool/main/h/hostname/hostname_%{version}.tar.gz

%description
This package provides commands which can be used to display the system's
DNS name, and to display or set its hostname or NIS domain name.

%prep
%setup -q -n hostname

sed -i 's/-o root -g root//g' Makefile
%build

make CFLAGS="-D_GNU_SOURCE $RPM_OPT_FLAGS $CFLAGS" CC=gcc 

%install
make BASEDIR=%{buildroot} BINDIR="/usr/bin" install

%files
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 23 2015 cjacker - 3.15-5
- Rebuild for new 4.0 release

