Summary: Simple interface for editing the font path for the X font server.
Name: chkfontpath
Version: 1.10.0
Release: 5
License: GPL
Source: %{name}-%{version}.tar.gz

%description 
This is a simple command line utility for configuring the directories
in the X font server's path.  It is mostly intended to be used
'internally' by RPM when packages with fonts are added or removed, but
it may be useful as a stand-alone utility in some instances.

%prep
%setup -q

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make INSTROOT=$RPM_BUILD_ROOT BINDIR=%{_sbindir} MANDIR=%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Fri Oct 23 2015 cjacker - 1.10.0-5
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

