Summary: SGPIO captive backplane tool
Name: sgpio
Version: 1.2.0.10
Release: 6 
License: GPLv2+
URL:    http://sources.redhat.com/lvm2/wiki/DMRAID_Eventing
Source: sgpio-1.2-0.10-src.tar.gz
Patch0: sgpio-1.2-makefile.patch

%description
Intel SGPIO enclosure management utility

%prep
%setup -q -n sgpio
%patch0 -p1 -b .makefile
chmod a-x *

%build
#@@@ workaround for #474755 - remove with next update
make clean
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" CC=clang

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT SBIN_DIR=$RPM_BUILD_ROOT%{_sbindir} MANDIR=$RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc README
%{_sbindir}/*
%{_mandir}/man1/sgpio.*

%changelog
* Fri Oct 23 2015 cjacker - 1.2.0.10-6
- Rebuild for new 4.0 release

