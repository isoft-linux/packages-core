%define byaccdate 20140527

Summary: A public domain Yacc parser generator
Name: byacc
Version: 1.9.%{byaccdate}
Release: 1
License: Public Domain
Group:  CoreDev/Development/Utility
URL: http://dickey.his.com/byacc/byacc.html
Source: ftp://invisible-island.net/byacc/byacc-%{byaccdate}.tgz

%description
Byacc (Berkeley Yacc) is a public domain LALR parser generator which
is used by many programs during their build process.

If you are going to do development on your system, you will want to install
this package.

%prep
%setup -q -n byacc-%{byaccdate}

%build
%configure --disable-dependency-tracking
make

%check
make check
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
ln -s yacc $RPM_BUILD_ROOT/usr/bin/byacc
mv yacc.1 $RPM_BUILD_ROOT/%{_mandir}/man1/byacc.1

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/yacc
/usr/bin/byacc
%{_mandir}/man1/yacc.1*
%{_mandir}/man1/byacc.1*


%changelog
* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
