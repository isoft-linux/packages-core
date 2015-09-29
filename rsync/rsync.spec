Summary: A program for synchronizing files over a network.
Name: rsync
Version: 3.1.1
Release: 1
Group: Applications/Internet
# TAG: for pre versions use
#Source:	ftp://rsync.samba.org/pub/rsync/rsync-%{version}pre1.tar.gz
Source:	ftp://rsync.samba.org/pub/rsync/rsync-%{version}.tar.gz
BuildRequires: libacl-devel, libattr-devel, autoconf, make, gcc
License: GPL

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

%prep
%setup -q

%build
%configure --with-included-zlib
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/rsync
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

